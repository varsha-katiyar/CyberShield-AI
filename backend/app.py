from flask import Flask, request, jsonify
from flask_cors import CORS
import requests # n8n se baat karne ke liye

app = Flask(__name__)
CORS(app)

# Demo n8n Webhook URL (Isme n8n se url paste karna hoga baad mein)
N8N_WEBHOOK_URL = "http://localhost:5678/webhook-test/shieldai-alert"

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    url = data.get('url', '')
    b = data.get('behavior_input', 0)
    n = data.get('nlp_input', 0)
    net = data.get('network_input', 0)

    # NLP Logic: Detect keyword in URL
    reasons = []
    nlp_boost = 0
    if "track" in url.lower() or "watch" in url.lower():
        nlp_boost = 20
        reasons.append("Suspicious keyword in URL")
    
    # Formula from PPT
    final_nlp = min(n + nlp_boost, 100)
    score = (0.4 * b) + (0.3 * final_nlp) + (0.3 * net)
    score = round(score, 2)

    status = "Safe ✅"
    if score > 70:
        status = "High Risk 🚨"
        reasons.append("Night activity spikes detected")
        # Trigger n8n Alert
        try:
            requests.post(N8N_WEBHOOK_URL, json={"alert": "High Risk Stalker", "score": score, "url": url})
        except:
            pass # n8n agar band ho toh error na aaye

    elif score > 30:
        status = "Suspicious ⚠️"

    return jsonify({
        'score': score,
        'status': status,
        'reasons': reasons if reasons else ["No immediate threat"]
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)