import os
import sqlite3
from pathlib import Path

from dotenv import load_dotenv
import psycopg2 as psycopg
import psycopg2.extras
import requests
from flask import Flask, jsonify, request
from flask_cors import CORS
from werkzeug.security import check_password_hash, generate_password_hash


# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app)

# Configure Google Gemini AI
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai_client = genai.Client(api_key=GEMINI_API_KEY)
else:
    genai_client = None
    print("Warning: GEMINI_API_KEY environment variable not set. Gemini AI features will not work.")

# N8N Webhook URL for email alerts
N8N_WEBHOOK_URL = "https://varshadev.app.n8n.cloud/webhook-test/42e49342-9eda-41ff-b95a-189ab77879ca"
SQLITE_DB_PATH = Path(__file__).with_name("cybershield_ai.db")
DB_INIT_ERROR = None
DB_BACKEND = None


def get_database_url():
    database_url = os.getenv("DATABASE_URL")
    if database_url:
        return database_url

    db_name = os.getenv("PGDATABASE", "cybershield_ai")
    db_user = os.getenv("PGUSER", "postgres")
    db_password = os.getenv("PGPASSWORD", "postgres")
    db_host = os.getenv("PGHOST", "localhost")
    db_port = os.getenv("PGPORT", "5432")

    return f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"


def get_postgres_connection():
    return psycopg.connect(get_database_url(), cursor_factory=psycopg2.extras.RealDictCursor, connect_timeout=3)


def get_sqlite_connection():
    conn = sqlite3.connect(SQLITE_DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_postgres():
    with get_postgres_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    full_name VARCHAR(120) NOT NULL,
                    email VARCHAR(255) UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
        conn.commit()


def init_sqlite():
    with get_sqlite_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conn.commit()


def init_db():
    global DB_INIT_ERROR, DB_BACKEND

    try:
        init_postgres()
        DB_BACKEND = "postgresql"
        DB_INIT_ERROR = None
        return
    except Exception as exc:
        DB_INIT_ERROR = str(exc)

    init_sqlite()
    DB_BACKEND = "sqlite"


def db_ready():
    return DB_BACKEND is not None


def db_error_response():
    return (
        jsonify(
            {
                "message": "Database not connected.",
                "details": DB_INIT_ERROR,
            }
        ),
        500,
    )


def row_to_user(row):
    if row is None:
        return None

    if isinstance(row, sqlite3.Row):
        row = dict(row)

    return {
        "id": row["id"],
        "full_name": row["full_name"],
        "email": row["email"],
        "created_at": row["created_at"],
    }


def find_user_by_email(email):
    if DB_BACKEND == "postgresql":
        with get_postgres_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT id, full_name, email, password_hash, created_at
                    FROM users
                    WHERE email = %s
                    """,
                    (email,),
                )
                return cur.fetchone()

    with get_sqlite_connection() as conn:
        cur = conn.execute(
            """
            SELECT id, full_name, email, password_hash, created_at
            FROM users
            WHERE email = ?
            """,
            (email,),
        )
        return cur.fetchone()


def create_user(full_name, email, password_hash):
    if DB_BACKEND == "postgresql":
        with get_postgres_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO users (full_name, email, password_hash)
                    VALUES (%s, %s, %s)
                    RETURNING id, full_name, email, created_at
                    """,
                    (full_name, email, password_hash),
                )
                user = cur.fetchone()
            conn.commit()
            return user

    with get_sqlite_connection() as conn:
        cur = conn.execute(
            """
            INSERT INTO users (full_name, email, password_hash)
            VALUES (?, ?, ?)
            """,
            (full_name, email, password_hash),
        )
        conn.commit()
        user_id = cur.lastrowid
        cur = conn.execute(
            """
            SELECT id, full_name, email, created_at
            FROM users
            WHERE id = ?
            """,
            (user_id,),
        )
        return cur.fetchone()


@app.route("/auth/register", methods=["POST"])
def register():
    if not db_ready():
        return db_error_response()

    data = request.get_json(silent=True) or {}
    full_name = data.get("full_name", "").strip()
    email = data.get("email", "").strip().lower()
    password = data.get("password", "")

    if not full_name or not email or not password:
        return jsonify({"message": "Full name, email, and password are required."}), 400

    if len(password) < 6:
        return jsonify({"message": "Password must be at least 6 characters long."}), 400

    password_hash = generate_password_hash(password)

    try:
        existing_user = find_user_by_email(email)
        if existing_user:
            return jsonify({"message": "An account with this email already exists."}), 409

        user = create_user(full_name, email, password_hash)
    except Exception as exc:
        return jsonify({"message": "Unable to register user.", "details": str(exc)}), 500

    backend_label = "PostgreSQL" if DB_BACKEND == "postgresql" else "SQLite"
    return (
        jsonify(
            {
                "message": f"Account created successfully. Stored in {backend_label}.",
                "user": row_to_user(user),
            }
        ),
        201,
    )


@app.route("/auth/login", methods=["POST"])
def login():
    if not db_ready():
        return db_error_response()

    data = request.get_json(silent=True) or {}
    email = data.get("email", "").strip().lower()
    password = data.get("password", "")

    if not email or not password:
        return jsonify({"message": "Email and password are required."}), 400

    try:
        user = find_user_by_email(email)
    except Exception as exc:
        return jsonify({"message": "Unable to log in.", "details": str(exc)}), 500

    if not user or not check_password_hash(user["password_hash"], password):
        return jsonify({"message": "Invalid email or password."}), 401

    return jsonify(
        {
            "message": "Login successful.",
            "user": row_to_user(user),
        }
    )


def get_gemini_reasoning(behavior_input, nlp_input, network_input, url, score, status):
    if not genai_client:
        return "Gemini AI not configured. Using default reasoning."
    
    try:
        prompt = f"""
        Analyze the following cybersecurity risk data and provide a brief, concise reason for the risk assessment:

        - Behavior Score: {behavior_input}/100
        - NLP Score: {nlp_input}/100  
        - Network Score: {network_input}/100
        - URL: {url}
        - Overall Risk Score: {score}/100
        - Risk Status: {status}

        Provide a short explanation (1-2 sentences) explaining why this activity might be risky or safe, focusing on patterns like unusual timing, suspicious keywords, or network behavior.
        """
        response = genai_client.models.generate_content(
            model='models/gemini-flash-latest',
            contents=prompt
        )
        return response.text.strip()
    except Exception as e:
        app.logger.error(f"Gemini API error: {str(e)}")
        print(f"Gemini API error: {str(e)}", flush=True)
        return "Unable to generate AI reasoning due to API error. Please verify your Gemini model configuration and API access."


@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json(silent=True) or {}
    url = data.get("url", "")
    behavior_input = data.get("behavior_input", 0)
    nlp_input = data.get("nlp_input", 0)
    network_input = data.get("network_input", 0)

    reasons = []
    nlp_boost = 0
    if "track" in url.lower() or "watch" in url.lower():
        nlp_boost = 20
        reasons.append("Suspicious keyword in URL")

    final_nlp = min(nlp_input + nlp_boost, 100)
    score = (0.4 * behavior_input) + (0.3 * final_nlp) + (0.3 * network_input)
    score = round(score, 2)

    status = "Safe"
    if score > 70:
        status = "High Risk"
    elif score > 30:
        status = "Suspicious"

    # Use Gemini for AI-powered reasoning
    ai_reason = get_gemini_reasoning(behavior_input, final_nlp, network_input, url, score, status)
    reasons.append(ai_reason)

    if score > 70:
        try:
            requests.post(
                N8N_WEBHOOK_URL,
                json={"alert": "High Risk Stalker", "score": score, "url": url},
                timeout=3,
            )
        except requests.RequestException:
            pass

    return jsonify(
        {
            "score": score,
            "status": status,
            "reasons": reasons if reasons else ["No immediate threat"],
        }
    )


@app.route("/health", methods=["GET"])
def health():
    return jsonify(
        {
            "status": "ok",
            "database": DB_BACKEND or "not-configured",
           "database_error": None if DB_BACKEND == "sqlite" else DB_INIT_ERROR
        }
    )


init_db()


if __name__ == "__main__":
    app.run(debug=True, port=5000)
