# CyberShield-AI: Google Gemini Integration Guide

## 🚀 Project Overview

CyberShield-AI is an advanced cybersecurity threat detection system that now integrates **Google Gemini AI** for intelligent threat analysis, risk assessment, and security recommendations. This makes the system stand out with cutting-edge AI capabilities.

## ✨ Key Features with AI Integration

### 1. **AI-Powered Threat Analysis** 🤖
- Real-time threat scoring using machine learning
- Behavioral anomaly detection
- NLP-based content analysis
- Network pattern recognition
- AI-generated risk assessments

### 2. **Intelligent Security Recommendations** 🛡️
- AI-powered actionable recommendations
- Immediate action items for high-risk threats
- Preventive measures based on threat patterns
- Monitoring suggestions customized to threat type

### 3. **URL Safety Assessment** 🔗
- AI analysis of domain reputation
- Phishing detection
- Malware risk identification
- SSL/certificate validation
- Safety scoring with detailed breakdown

### 4. **Anomaly Explanation** 📊
- Natural language explanations of detected anomalies
- Context-aware threat descriptions
- Security professional-friendly reporting

## 🔧 Setup Instructions

### Prerequisites
- Python 3.12+
- Node.js 18+
- Google Account with AI API access
- PostgreSQL (optional, SQLite fallback available)

### Step 1: Get Google API Key

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Click "Create API Key"
3. Copy your API key

### Step 2: Backend Setup

```bash
# Clone and navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Add your Google API Key to .env
# GOOGLE_API_KEY=your_api_key_here

# Run backend
python app.py
```

### Step 3: Frontend Setup

```bash
# Navigate to frontend
cd ../frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Backend will be running on `http://localhost:5000`
Frontend will be running on `http://localhost:5173`

## 📚 API Endpoints

### Analysis Endpoints

#### 1. **Run Threat Analysis**
```bash
POST /analyze
Content-Type: application/json

{
  "behavior_input": 65,        # Behavioral score (0-100)
  "nlp_input": 45,             # NLP/Content score (0-100)
  "network_input": 75,         # Network score (0-100)
  "url": "https://example.com" # Optional URL to analyze
}

Response:
{
  "score": 62.5,
  "status": "Suspicious",
  "reasons": ["Suspicious keyword in URL"],
  "ai_powered": true,
  "ai_analysis": {
    "overall_risk_level": "high",
    "risk_score": 72,
    "threat_summary": "...",
    "threat_indicators": [...],
    "key_insights": [...]
  }
}
```

#### 2. **Get AI Recommendations**
```bash
POST /ai/recommendations
Content-Type: application/json

{
  "threat_level": "high",
  "threat_details": {
    "overall_risk_level": "high",
    "threat_indicators": ["Behavioral spike detected"],
    ...
  }
}

Response:
{
  "success": true,
  "recommendations": {
    "immediate_actions": [
      "Block suspicious IP addresses",
      "Review recent user activities"
    ],
    "preventive_measures": [
      "Implement rate limiting",
      "Enable 2FA for all accounts"
    ],
    "monitoring_suggestions": [
      "Monitor login patterns",
      "Track data access"
    ]
  }
}
```

#### 3. **Assess URL Safety**
```bash
POST /ai/assess-url
Content-Type: application/json

{
  "url": "https://example.com"
}

Response:
{
  "success": true,
  "assessment": {
    "safety_score": 85,
    "risk_level": "safe",
    "concerns": [],
    "recommendations": ["Site appears legitimate"]
  }
}
```

#### 4. **Explain Anomaly**
```bash
POST /ai/explain-anomaly
Content-Type: application/json

{
  "anomaly_data": {
    "type": "behavioral_spike",
    "severity": "high",
    "timestamp": "2024-01-15T10:30:00Z"
  }
}

Response:
{
  "success": true,
  "explanation": "This behavioral spike suggests unusual account activity patterns that deviate from the user's baseline behavior..."
}
```

#### 5. **Health Check**
```bash
GET /health

Response:
{
  "status": "ok",
  "database": "postgresql",
  "ai_service": "available"
}
```

## 🎨 Frontend Features

### Dashboard Components

1. **Input Studio**
   - Adjust threat parameters with sliders
   - Input URL for analysis
   - Real-time visualization

2. **Live Insights**
   - Behavior activity chart
   - Threat score display
   - AI-powered risk assessment
   - Status indicators (Safe/Suspicious/High Risk)

3. **AI Analysis Panel** (New)
   - Real-time AI-powered threat analysis
   - Risk level and score from Gemini
   - Threat indicators
   - Confidence levels

4. **Security Recommendations** (New)
   - Immediate action items
   - Preventive measures
   - Monitoring suggestions
   - All powered by Gemini AI

5. **URL Safety Assessment** (New)
   - Safety score visualization
   - Risk level indicators
   - Domain concerns
   - Actionable recommendations

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Frontend (React)                      │
│  - User authentication                                  │
│  - Dashboard with threat parameters                     │
│  - Real-time AI insights display                        │
└──────────────────┬──────────────────────────────────────┘
                   │ HTTP/REST
                   ↓
┌─────────────────────────────────────────────────────────┐
│              Backend API (Flask)                         │
│  - /analyze - Threat analysis endpoint                  │
│  - /ai/* - AI-powered endpoints                         │
│  - /auth/* - User authentication                        │
└──────────┬──────────────────────┬──────────────────────┘
           │                      │
           ↓                      ↓
    ┌─────────────┐       ┌──────────────────┐
    │  PostgreSQL/│       │  Google Gemini   │
    │  SQLite DB  │       │  API (via SDK)   │
    └─────────────┘       └──────────────────┘
```

## 🔐 Environment Variables

Required environment variables (create `.env` in backend folder):

```env
# Google Cloud AI (REQUIRED)
GOOGLE_API_KEY=your_api_key_here

# Database
DATABASE_URL=postgresql://user:password@localhost/cybershield_ai
# Or individual components:
PGHOST=localhost
PGPORT=5432
PGDATABASE=cybershield_ai
PGUSER=postgres
PGPASSWORD=postgres

# Flask
FLASK_ENV=development
FLASK_DEBUG=True

# N8N Webhook (optional, for alerts)
N8N_WEBHOOK_URL=http://localhost:5678/webhook-test/shieldai-alert
```

## 📊 Data Flow

1. **User Input** → Frontend collects threat parameters
2. **Analysis Request** → Sent to backend /analyze endpoint
3. **Threat Calculation** → Backend calculates initial threat score
4. **AI Analysis** → Calls Gemini API for intelligent analysis
5. **AI Recommendations** → Gets actionable recommendations
6. **URL Assessment** → Analyzes URL if provided
7. **Response** → Frontend displays all insights
8. **Alerts** → High-risk alerts sent to n8n webhook

## 🚀 Deployment

### Local Development
```bash
# Terminal 1: Backend
cd backend
python app.py

# Terminal 2: Frontend
cd frontend
npm run dev
```

### Google Cloud Run (Production)
See [GOOGLE_CLOUD_DEPLOYMENT.md](./GOOGLE_CLOUD_DEPLOYMENT.md) for complete deployment guide.

Quick deployment:
```bash
cd backend
gcloud run deploy cybershield-backend \
  --source . \
  --set-env-vars GOOGLE_API_KEY="your_key" \
  --allow-unauthenticated
```

## 📈 Performance & Optimization

### Caching Strategy
- Cache Gemini responses for similar threats
- Use Redis for session caching (optional)
- Minimize API calls with batch analysis

### Rate Limiting
- Implement rate limiting on API endpoints
- Gemini API has quotas - monitor usage
- Add queue system for high-volume requests

### Cost Optimization
- Gemini API is free with limits
- Monitor usage: https://console.cloud.google.com/apis/api/generativeai.googleapis.com/quotas
- Implement caching to reduce redundant calls

## 🛡️ Security Considerations

1. **API Keys**
   - Never commit .env files
   - Use environment variables
   - Rotate keys regularly
   - Use Secret Manager in production

2. **Data Protection**
   - HTTPS only in production
   - Encrypt sensitive data
   - Implement CORS properly
   - Validate all inputs

3. **Authentication**
   - Implement JWT or session tokens
   - Secure password hashing
   - Enable 2FA (recommended)

4. **Monitoring**
   - Log all API calls
   - Monitor for suspicious patterns
   - Set up alerts
   - Regular security audits

## 🐛 Troubleshooting

### "GOOGLE_API_KEY not set" Error
```bash
# Make sure .env file exists in backend folder
# Copy from .env.example and add your key
cp .env.example .env
# Edit .env and add: GOOGLE_API_KEY=your_key
```

### Connection Refused Error
```bash
# Check if backend is running
# Make sure Flask app is running on port 5000
python app.py

# Check if frontend is trying to reach correct backend URL
# Should be http://127.0.0.1:5000
```

### AI Service Not Available
```bash
# Check API key is valid
# Visit https://makersuite.google.com/app/apikey
# Verify key is in .env file
# Check internet connection
```

### Gemini API Rate Limiting
- Free tier allows ~30 requests per minute
- Upgrade for higher quotas
- Implement caching to reduce requests

## 📚 Additional Resources

- [Google Gemini API Docs](https://ai.google.dev/docs)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [React Documentation](https://react.dev/)
- [Cloud Run Deployment Guide](./GOOGLE_CLOUD_DEPLOYMENT.md)

## 🤝 Contributing

To enhance the AI integration:

1. Add new AI analysis models
2. Improve threat scoring algorithm
3. Add more AI endpoints
4. Enhance UI with more insights
5. Implement caching strategy
6. Add test coverage

## 📝 License

[Add your license information here]

## 🎯 What Makes This Stand Out

1. **Real-time AI Analysis**: Leverages Google's Gemini AI for instant threat assessment
2. **Intelligent Recommendations**: AI-generated, actionable security recommendations
3. **Multi-dimensional Analysis**: Combines behavioral, NLP, and network analysis
4. **Cloud-Ready**: Built for scalable deployment on Google Cloud Platform
5. **User-Friendly**: Beautiful dashboard with real-time AI insights
6. **Production-Grade**: Includes deployment guides, security best practices, and monitoring

## 📞 Support

For issues or questions:
1. Check [Troubleshooting](#-troubleshooting) section
2. Review error logs: `gcloud run logs read cybershield-backend`
3. Check API health: `curl http://localhost:5000/health`
