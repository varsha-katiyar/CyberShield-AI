# CyberShield AI 🛡️

> **Revolutionizing Cyber Threat Detection with AI-Powered Real-Time Analysis**

CyberShield AI is an advanced threat detection platform that analyzes social media profiles and behavior patterns in real-time. Built for security professionals and organizations, it provides instant risk assessment with automated alerting capabilities.

## 🚀 Key Highlights

- **Duality AI Simulation**: Experience synthetic data handling with our "Stalker Attack" demo
- **Real-Time Scoring**: Instant threat analysis with visual feedback
- **Automated Workflows**: n8n-powered email alerts to administrators
- **Interactive Dashboard**: Sleek UI with live charts and animations
- **Explainable AI**: Transparent reasoning for every threat score

## 🏗️ Architecture Overview

Our microservices architecture ensures scalability and modularity:

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   React UI      │    │   Flask API     │    │   n8n Workflow  │    │   Gmail API     │
│                 │    │                 │    │                 │    │                 │
│ • User Controls │───▶│ • Threat Scoring│───▶│ • Alert Logic   │───▶│ • Email Alerts │
│ • Live Charts   │    │ • AI Processing │    │ • Automation    │    │ • Notifications│
│ • Visual Feedback│    │ • Data Validation│    │ • Webhooks     │    │ • Templates    │
└─────────────────┘    └─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Data Flow

1. **Input Collection**: User adjusts risk parameters via intuitive sliders
2. **Analysis Engine**: Flask backend processes inputs with AI algorithms
3. **Alert System**: n8n triggers automated workflows based on threat levels
4. **Notification**: Gmail integration sends instant alerts to security teams
5. **Visualization**: Results displayed with animated charts and status indicators

## 🛠️ Tech Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Frontend** | React + Custom CSS | Interactive dashboard with real-time updates |
| **Backend** | Flask (Python) | RESTful API for threat analysis |
| **Automation** | n8n | Workflow orchestration and email alerts |
| **Database** | MongoDB | Data storage for analysis logs |
| **Deployment** | Docker | Containerized deployment (optional) |

## ✨ Features

### Core Functionality
- **Multi-Parameter Analysis**: Behavior, NLP, and Network risk assessment
- **Dynamic Scoring**: Real-time threat score calculation (0-100%)
- **Visual Analytics**: Interactive line charts and pie charts
- **Activity Logging**: Timestamped security event tracking

### Advanced Features
- **Duality Simulation**: One-click demo of high-risk scenarios
- **Responsive Design**: Optimized for desktop and mobile devices
- **Dark Theme**: Professional security-focused UI
- **Animated Feedback**: Smooth transitions and visual alerts

### Security Features
- **Automated Alerts**: Instant email notifications for high-risk detections
- **Risk Classification**: Color-coded results (Green/Safe, Red/Alert)
- **Explainable Results**: Detailed reasoning for each analysis

## 📦 Installation & Setup

### Prerequisites
- **Node.js** v16+ (for frontend)
- **Python** v3.8+ (for backend)
- **MongoDB** (local or cloud instance)
- **n8n** (for workflow automation)

### Quick Start

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/cybershield-ai.git
   cd cybershield-ai
   ```

2. **Backend Setup**
   ```bash
   cd backend
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS/Linux
   # source venv/bin/activate

   pip install -r requirements.txt
   python app.py
   ```

3. **Frontend Setup**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

4. **n8n Configuration**
   ```bash
   npm install -g n8n
   n8n start
   # Import workflow from n8n-workflow.json
   # Configure Gmail credentials in n8n
   ```

5. **Access the Application**
   - Frontend: `http://localhost:5173`
   - Backend API: `http://localhost:5000`

## 🎯 Usage Guide

### Basic Analysis
1. Enter a social media profile URL
2. Adjust the three risk sliders (Behavior, NLP, Network)
3. Click "RUN REAL-TIME ANALYSIS"
4. View the threat score and reasoning

### Duality Simulation
- Click "DUALITY SIMULATION" to see a high-risk stalker attack scenario
- Observe how sliders auto-adjust and alerts trigger

### Understanding Results
- **Green Results**: Low risk profiles
- **Red Results**: High risk with flashing alerts
- **Charts Update**: Real-time visualization of threat patterns

## 📡 API Reference

### POST /analyze
Analyzes threat parameters and returns risk assessment.

**Request Body:**
```json
{
  "behavior_input": 85,
  "nlp_input": 72,
  "network_input": 90,
  "url": "https://instagram.com/example"
}
```

**Response:**
```json
{
  "score": 87,
  "status": "High Risk Detected",
  "reasons": ["High behavior risk", "Suspicious network activity"]
}
```

## 🔧 Development

### Project Structure
```
cybershield-ai/
├── backend/          # Flask API server
│   ├── app.py       # Main application
│   ├── requirements.txt
│   └── venv/        # Virtual environment
├── frontend/         # React dashboard
│   ├── src/
│   │   ├── App.jsx
│   │   ├── App.css
│   │   └── main.jsx
│   ├── package.json
│   └── vite.config.js
├── n8n-workflow.json # Automation workflow
└── README.md
```

### Building for Production
```bash
# Frontend
cd frontend
npm run build

# Backend (if needed)
cd backend
python -m py_compile app.py
```

## 🚀 Deployment

### Docker (Recommended)
```bash
# Build images
docker build -t cybershield-frontend ./frontend
docker build -t cybershield-backend ./backend

# Run containers
docker-compose up
```

### Cloud Deployment
- **Frontend**: Vercel, Netlify
- **Backend**: Heroku, AWS Elastic Beanstalk
- **Database**: MongoDB Atlas
- **Automation**: n8n Cloud

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines
- Follow React best practices
- Write clean, documented Python code
- Test all new features
- Update documentation

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Contact

**CyberShield AI Team**
- Email: team@cybershield.ai
- GitHub: [@cybershield-ai](https://github.com/cybershield-ai)

---

*Built with  for a safer digital world*

## License

MIT License - see LICENSE file for details