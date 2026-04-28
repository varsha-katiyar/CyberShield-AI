import os
import sqlite3
from pathlib import Path

import psycopg
import requests
from flask import Flask, jsonify, request
from flask_cors import CORS
from psycopg.rows import dict_row
from werkzeug.security import check_password_hash, generate_password_hash
from dotenv import load_dotenv

from ai_service import get_ai_service

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app)

N8N_WEBHOOK_URL = "http://localhost:5678/webhook-test/shieldai-alert"
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
    return psycopg.connect(get_database_url(), row_factory=dict_row, connect_timeout=3)


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


def _get_fallback_recommendations(threat_level: str) -> dict:
    """Generate fallback recommendations when AI service is unavailable"""
    threat_level = str(threat_level).lower().strip()
    
    recommendations = {
        "critical": {
            "immediate_actions": [
                "Isolate affected system from network immediately",
                "Preserve forensic evidence and initiate incident response",
                "Notify security team and stakeholders",
                "Activate business continuity procedures"
            ],
            "preventive_measures": [
                "Implement additional network segmentation and monitoring",
                "Strengthen multi-factor authentication",
                "Conduct immediate security audit and patch management",
                "Deploy advanced threat detection systems"
            ],
            "monitoring_suggestions": [
                "Enable 24/7 monitoring on critical systems",
                "Track all access and anomalous behavior patterns",
                "Set up real-time alerting for similar threats",
                "Review and strengthen incident response procedures"
            ],
            "risk_explanation": "Critical threat requires immediate action to prevent system compromise."
        },
        "high": {
            "immediate_actions": [
                "Conduct detailed threat assessment and analysis",
                "Implement temporary security controls",
                "Document all findings and evidence",
                "Prepare incident response and mitigation plan"
            ],
            "preventive_measures": [
                "Apply security patches and updates",
                "Strengthen access controls and authentication",
                "Increase system monitoring and logging",
                "Review and update security policies"
            ],
            "monitoring_suggestions": [
                "Increase monitoring frequency on affected systems",
                "Track recurring threat patterns and indicators",
                "Review security logs and audit trails daily",
                "Conduct regular incident response drills"
            ],
            "risk_explanation": "High-level threat requires prompt investigation and mitigation actions."
        },
        "medium": {
            "immediate_actions": [
                "Investigate threat source and nature",
                "Document findings and impact assessment",
                "Consider and implement security updates",
                "Review user access permissions"
            ],
            "preventive_measures": [
                "Keep systems updated with latest patches",
                "Implement security best practices",
                "Conduct security awareness training",
                "Review and strengthen access controls"
            ],
            "monitoring_suggestions": [
                "Monitor system performance and activity",
                "Review security logs on regular schedule",
                "Track security metrics and trends",
                "Test backup and recovery procedures"
            ],
            "risk_explanation": "Medium-level threat should be addressed with standard security measures."
        },
        "low": {
            "immediate_actions": [
                "Continue monitoring the situation",
                "Apply routine security updates",
                "Document observations for records",
                "Maintain standard security practices"
            ],
            "preventive_measures": [
                "Maintain current security posture",
                "Apply updates and patches as scheduled",
                "Continue security training programs",
                "Keep security policies updated"
            ],
            "monitoring_suggestions": [
                "Continue standard system monitoring",
                "Review logs as per normal schedule",
                "Maintain security hygiene practices",
                "Track overall system health"
            ],
            "risk_explanation": "Low-level threat - maintain standard security practices and monitoring."
        }
    }
    
    return recommendations.get(threat_level, recommendations["medium"])


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
        reasons.append("Night activity spikes detected")
        try:
            requests.post(
                N8N_WEBHOOK_URL,
                json={"alert": "High Risk Stalker", "score": score, "url": url},
                timeout=3,
            )
        except requests.RequestException:
            pass
    elif score > 30:
        status = "Suspicious"

    # Get AI analysis from Gemini
    ai_analysis = None
    ai_service = get_ai_service()
    if ai_service:
        ai_result = ai_service.analyze_threat(
            behavior_input, nlp_input, network_input, url
        )
        if ai_result.get("success"):
            ai_analysis = ai_result.get("threat_analysis")

    return jsonify(
        {
            "score": score,
            "status": status,
            "reasons": reasons if reasons else ["No immediate threat"],
            "ai_analysis": ai_analysis,
            "ai_powered": ai_analysis is not None,
        }
    )




@app.route("/ai/recommendations", methods=["POST"])
def get_ai_recommendations():
    """Get AI-powered security recommendations based on threat analysis"""
    data = request.get_json(silent=True) or {}
    threat_level = data.get("threat_level", "medium")
    threat_details = data.get("threat_details", {})

    ai_service = get_ai_service()
    if not ai_service:
        # Return fallback recommendations when AI service is not available
        fallback_recs = _get_fallback_recommendations(threat_level)
        return jsonify({
            "success": False,
            "error": "AI service not configured, using fallback recommendations.",
            "recommendations": fallback_recs,
        })

    result = ai_service.generate_security_recommendations(threat_level, threat_details)
    # Ensure we always return recommendations
    if not result.get("recommendations"):
        result["recommendations"] = _get_fallback_recommendations(threat_level)
    return jsonify(result)


@app.route("/ai/explain-anomaly", methods=["POST"])
def explain_anomaly():
    """Get AI-powered explanation of detected anomalies"""
    data = request.get_json(silent=True) or {}
    anomaly_data = data.get("anomaly_data", {})

    ai_service = get_ai_service()
    if not ai_service:
        return (
            jsonify(
                {
                    "success": False,
                    "error": "AI service not configured. Set GOOGLE_API_KEY environment variable.",
                }
            ),
            503,
        )

    explanation = ai_service.explain_anomaly(anomaly_data)
    return jsonify({"success": True, "explanation": explanation})


@app.route("/ai/assess-url", methods=["POST"])
def assess_url():
    """Get AI-powered URL safety assessment"""
    data = request.get_json(silent=True) or {}
    url = data.get("url", "")

    if not url:
        return jsonify({"success": False, "error": "URL is required"}), 400

    ai_service = get_ai_service()
    if not ai_service:
        return (
            jsonify(
                {
                    "success": False,
                    "error": "AI service not configured. Set GOOGLE_API_KEY environment variable.",
                }
            ),
            503,
        )

    result = ai_service.assess_url_safety(url)
    return jsonify(result)


@app.route("/health", methods=["GET"])
def health():
    ai_service = get_ai_service()
    return jsonify(
        {
            "status": "ok",
            "database": DB_BACKEND or "not-configured",
            "database_error": DB_INIT_ERROR,
            "ai_service": "available" if ai_service else "not-configured",
        }
    )


init_db()


if __name__ == "__main__":
   app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
