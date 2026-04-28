# 🚀 Quick Start Guide - CyberShield-AI with Google Gemini

## 5-Minute Setup

### Step 1: Get Google API Key (2 minutes)
1. Go to https://makersuite.google.com/app/apikey
2. Click "Create API Key"
3. Copy the key

### Step 2: Set Up Backend (2 minutes)

**Windows:**
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
# Edit .env and add your GOOGLE_API_KEY
python app.py
```

**macOS/Linux:**
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env and add your GOOGLE_API_KEY
python app.py
```

### Step 3: Set Up Frontend (1 minute)

**In a new terminal:**
```bash
cd frontend
npm install
npm run dev
```

### Step 4: Open in Browser
- Frontend: http://localhost:5173
- Backend API: http://localhost:5000
- Health Check: http://localhost:5000/health

## 🎮 Testing the AI Features

### Test Threat Analysis with AI
```bash
curl -X POST http://localhost:5000/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "behavior_input": 75,
    "nlp_input": 60,
    "network_input": 80,
    "url": "https://suspicious-example.com"
  }'
```

### Get AI Recommendations
```bash
curl -X POST http://localhost:5000/ai/recommendations \
  -H "Content-Type: application/json" \
  -d '{
    "threat_level": "high",
    "threat_details": {
      "overall_risk_level": "high",
      "threat_indicators": ["Behavioral spike detected", "Network anomaly"]
    }
  }'
```

### Assess URL Safety
```bash
curl -X POST http://localhost:5000/ai/assess-url \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com"
  }'
```

## 🎯 Key Features to Try

1. **Threat Analysis Dashboard**
   - Adjust sliders to change threat scores
   - Enter a URL to analyze
   - Click "RUN REAL-TIME ANALYSIS"
   - Watch AI analysis appear in real-time

2. **AI-Powered Recommendations**
   - Based on threat level
   - Lists immediate actions
   - Provides preventive measures
   - Suggests monitoring strategies

3. **URL Safety Assessment**
   - Automatic when you provide a URL
   - Shows safety score (0-100)
   - Lists specific concerns
   - Provides recommendations

## 📂 File Structure

```
CyberShield-AI/
├── backend/                    # Flask API
│   ├── app.py                 # Main Flask app
│   ├── ai_service.py          # Gemini AI integration (NEW)
│   ├── requirements.txt        # Python dependencies (UPDATED)
│   ├── Dockerfile            # For Cloud Run (NEW)
│   └── .env.example           # Config template
├── frontend/                   # React app
│   ├── src/
│   │   ├── App.jsx           # Main component (UPDATED)
│   │   ├── App.css           # Styles (UPDATED)
│   │   └── main.jsx
│   └── package.json
├── AI_INTEGRATION_GUIDE.md    # Detailed documentation (NEW)
├── GOOGLE_CLOUD_DEPLOYMENT.md # Cloud deployment guide (NEW)
└── .gitignore                 # Git config (UPDATED)
```

## 🔑 Environment Variables (.env)

```env
# REQUIRED: Your Google API Key
GOOGLE_API_KEY=your_api_key_here

# Database (optional - defaults to SQLite)
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/cybershield_ai

# N8N webhook (optional)
N8N_WEBHOOK_URL=http://localhost:5678/webhook-test/shieldai-alert
```

## 🐛 Common Issues

| Issue | Solution |
|-------|----------|
| "GOOGLE_API_KEY not set" | Add `GOOGLE_API_KEY=...` to `.env` file |
| "Cannot connect to backend" | Check port 5000 is free, run `python app.py` |
| "npm: command not found" | Install Node.js from nodejs.org |
| "AI features not working" | Verify API key is valid at makersuite.google.com |

## 📊 What's New

### Backend Changes
- ✅ Added `ai_service.py` with Gemini AI integration
- ✅ New endpoints: `/ai/recommendations`, `/ai/assess-url`, `/ai/explain-anomaly`
- ✅ Enhanced `/analyze` with AI-powered insights
- ✅ Updated requirements.txt with Google AI libraries
- ✅ Added Dockerfile for Cloud deployment

### Frontend Changes
- ✅ Enhanced threat analysis display with AI insights
- ✅ New AI Recommendations panel
- ✅ New URL Safety Assessment panel
- ✅ Real-time loading states
- ✅ Beautiful styling for AI components

### Documentation
- ✅ This quick start guide
- ✅ Comprehensive AI integration guide
- ✅ Google Cloud deployment guide
- ✅ Updated .env.example

## 🚀 Next Steps

1. **Deploy to Google Cloud**
   - Follow [GOOGLE_CLOUD_DEPLOYMENT.md](./GOOGLE_CLOUD_DEPLOYMENT.md)
   - Get your app running on Cloud Run
   - Connect to Cloud SQL or Firestore

2. **Customize AI Analysis**
   - Modify prompts in `ai_service.py`
   - Add new analysis endpoints
   - Implement caching for better performance

3. **Enhance Frontend**
   - Add more visualizations
   - Implement user preferences
   - Create reporting features

4. **Production Readiness**
   - Add authentication
   - Set up monitoring
   - Configure error tracking
   - Implement rate limiting

## 📞 Need Help?

1. Check the [AI_INTEGRATION_GUIDE.md](./AI_INTEGRATION_GUIDE.md) for detailed docs
2. Review API responses in browser console
3. Check backend logs in terminal
4. Verify API key at https://makersuite.google.com/app/apikey

## 💡 Pro Tips

- Start with lower threat scores to see how AI interprets them
- The AI learns from patterns - feed it diverse threat scenarios
- Cache AI responses to reduce API usage
- Monitor your API quota at console.cloud.google.com
- Use the health check endpoint to verify setup: `curl http://localhost:5000/health`

## 🎉 You're All Set!

Your CyberShield-AI with Google Gemini is now running. Go to http://localhost:5173 and start analyzing threats with AI!
