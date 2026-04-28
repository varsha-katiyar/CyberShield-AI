import { useEffect, useState } from 'react'
import axios from 'axios'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts'
import './App.css'

const API_BASE_URL = 'https://cybershield-ai-backend.onrender.com/'
const AUTH_STORAGE_KEY = 'cybershield-user'

const emptyAuthForm = {
  full_name: '',
  email: '',
  password: '',
}

function App() {
  const [authMode, setAuthMode] = useState('login')
  const [authForm, setAuthForm] = useState(emptyAuthForm)
  const [authMessage, setAuthMessage] = useState('')
  const [authLoading, setAuthLoading] = useState(false)
  const [user, setUser] = useState(null)
  const [inputs, setInputs] = useState({ behavior: 50, nlp: 50, network: 50, url: '' })
  const [result, setResult] = useState(null)
  const [aiRecommendations, setAiRecommendations] = useState(null)
  const [urlAssessment, setUrlAssessment] = useState(null)
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    const storedUser = localStorage.getItem(AUTH_STORAGE_KEY)
    if (storedUser) {
      try {
        setUser(JSON.parse(storedUser))
      } catch {
        localStorage.removeItem(AUTH_STORAGE_KEY)
      }
    }
  }, [])

  const chartData = [
    { time: '10pm', activity: 22 },
    { time: '12am', activity: inputs.behavior > 60 ? 83 : 42 },
    { time: '02am', activity: inputs.behavior > 80 ? 97 : 53 },
    { time: '04am', activity: 31 },
  ]

  const pieData = [
    { name: 'Low Risk', value: 45, color: '#10b981' },
    { name: 'Medium Risk', value: 30, color: '#f59e0b' },
    { name: 'High Risk', value: 25, color: '#ef4444' },
  ]

  const activityLog = [
    { time: '2:30 PM', event: 'High Risk Profile Detected' },
    { time: '2:31 PM', event: 'Alert Email Sent to Admin' },
    { time: '2:32 PM', event: 'User Notification Dispatched' },
  ]

  const updateInput = (key) => (event) => {
    const value = key === 'url' ? event.target.value : Number(event.target.value)
    setInputs({ ...inputs, [key]: value })
  }

  const updateAuthForm = (key) => (event) => {
    setAuthForm({ ...authForm, [key]: event.target.value })
  }

  const switchAuthMode = (mode) => {
    setAuthMode(mode)
    setAuthMessage('')
    setAuthForm(emptyAuthForm)
  }

  const persistUser = (nextUser) => {
    setUser(nextUser)
    localStorage.setItem(AUTH_STORAGE_KEY, JSON.stringify(nextUser))
  }

  const handleAuthSubmit = async (event) => {
    event.preventDefault()
    setAuthLoading(true)
    setAuthMessage('')

    const endpoint = authMode === 'login' ? '/auth/login' : '/auth/register'
    const payload =
      authMode === 'login'
        ? { email: authForm.email, password: authForm.password }
        : {
            full_name: authForm.full_name,
            email: authForm.email,
            password: authForm.password,
          }

    try {
      const response = await axios.post(`${API_BASE_URL}${endpoint}`, payload)
      persistUser(response.data.user)
      setAuthMessage(response.data.message)
      setAuthForm(emptyAuthForm)
    } catch (error) {
      const serverMessage = error.response?.data?.message
      const serverDetails = error.response?.data?.details

      setAuthMessage(
        serverMessage
          ? serverDetails
            ? `${serverMessage} ${serverDetails}`
            : serverMessage
          : 'Unable to connect to backend right now.',
      )
    } finally {
      setAuthLoading(false)
    }
  }

  const handleLogout = () => {
    localStorage.removeItem(AUTH_STORAGE_KEY)
    setUser(null)
    setResult(null)
    setAuthMode('login')
    setAuthMessage('')
  }

  const simulateStalkerAttack = () => {
    setInputs({
      behavior: 95,
      nlp: 92,
      network: 98,
      url: inputs.url || 'instagr.am/spy_user',
    })
    setResult({
      score: 93,
      status: 'Stalker Attack Detected',
      reasons: ['High behavior risk', 'Rapid NLP escalation', 'Suspicious network activity'],
    })
  }

  const analyzeData = async () => {
    setLoading(true)
    setAiRecommendations(null)
    setUrlAssessment(null)
    try {
      const response = await axios.post(`${API_BASE_URL}/analyze`, {
        behavior_input: inputs.behavior,
        nlp_input: inputs.nlp,
        network_input: inputs.network,
        url: inputs.url,
      })
      setResult(response.data)

      // Get AI recommendations - always try to get them
      try {
        const threatLevel = response.data.ai_analysis?.overall_risk_level || 
                           (response.data.score > 70 ? 'high' : response.data.score > 30 ? 'medium' : 'low')
        
        const recResponse = await axios.post(`${API_BASE_URL}/ai/recommendations`, {
          threat_level: threatLevel,
          threat_details: response.data.ai_analysis || {
            risk_score: response.data.score,
            status: response.data.status
          },
        })
        
        // Use recommendations from response, regardless of success status
        if (recResponse.data && recResponse.data.recommendations) {
          setAiRecommendations(recResponse.data.recommendations)
          console.log('Recommendations loaded:', recResponse.data.recommendations)
        }
      } catch (err) {
        console.error('AI recommendations error:', {
          message: err.message,
          status: err.response?.status,
          data: err.response?.data
        })
      }

      // Assess URL if provided
      if (inputs.url && inputs.url.trim()) {
        try {
          const urlResponse = await axios.post(`${API_BASE_URL}/ai/assess-url`, {
            url: inputs.url,
          })
          if (urlResponse.data.success && urlResponse.data.assessment) {
            setUrlAssessment(urlResponse.data.assessment)
          }
        } catch (err) {
          console.error('URL assessment error:', err.message)
        }
      }
    } catch (error) {
      console.error('Analysis error:', error)
      alert('Backend not connected. Please start python app.py and try again.')
    } finally {
      setLoading(false)
    }
  }

  if (!user) {
    return (
      <div className="app-shell auth-shell">
        <div className="app-background">
          <div className="bg-glow glow-1" />
          <div className="bg-glow glow-2" />
          <div className="bg-orbit orbit-1" />
          <div className="bg-orbit orbit-2" />
          <div className="bg-grid" />
        </div>

        <main className="auth-layout">
          <section className="hero-panel auth-hero">
            <div className="auth-hero-copy">
              <div className="brand-mark">
                <span className="brand-icon">CS</span>
                <div>
                  <p className="eyebrow">CyberShield AI</p>
                </div>
              </div>
              <h1>Please sign in or create an account first</h1>
            </div>

            <div className="hero-visual">
              <div className="visual-ring ring-a" />
              <div className="visual-ring ring-b" />
              <div className="visual-ring ring-c" />
              <div className="visual-core">
                <span className="core-label">Shielded Access</span>
                <strong>Trusted entry before dashboard access</strong>
              </div>
              <div className="visual-chip chip-a">Account</div>
              <div className="visual-chip chip-b">Security</div>
              <div className="visual-chip chip-c">Insights</div>
            </div>
          </section>

          <section className="panel auth-panel">
            <div className="auth-toggle">
              <button
                className={authMode === 'login' ? 'toggle-chip active' : 'toggle-chip'}
                onClick={() => switchAuthMode('login')}
                type="button"
              >
                Sign In
              </button>
              <button
                className={authMode === 'register' ? 'toggle-chip active' : 'toggle-chip'}
                onClick={() => switchAuthMode('register')}
                type="button"
              >
                Create Account
              </button>
            </div>

            <div className="panel-heading auth-heading">
              <span className="panel-badge">{authMode === 'login' ? 'Welcome back' : 'New account'}</span>
              <h2>{authMode === 'login' ? 'Login to continue' : 'Register before entering'}</h2>
            </div>

            <form className="auth-form" onSubmit={handleAuthSubmit}>
              {authMode === 'register' && (
                <div className="control-group">
                  <label htmlFor="full-name">Full Name</label>
                  <input
                    id="full-name"
                    type="text"
                    placeholder="Enter your full name"
                    value={authForm.full_name}
                    onChange={updateAuthForm('full_name')}
                    className="text-input"
                    required
                  />
                </div>
              )}

              <div className="input-shell">
                <span className="input-caption">Identity</span>
                <div className="control-group">
                  <label htmlFor="email">Email Address</label>
                  <input
                    id="email"
                    type="email"
                    placeholder="name@example.com"
                    value={authForm.email}
                    onChange={updateAuthForm('email')}
                    className="text-input"
                    required
                  />
                </div>
              </div>

              <div className="input-shell">
                <span className="input-caption">Security</span>
                <div className="control-group">
                  <label htmlFor="password">Password</label>
                  <input
                    id="password"
                    type="password"
                    placeholder="Minimum 6 characters"
                    value={authForm.password}
                    onChange={updateAuthForm('password')}
                    className="text-input"
                    required
                  />
                </div>
              </div>

              {authMessage && <div className="auth-message">{authMessage}</div>}

              <button className="button-primary" type="submit" disabled={authLoading}>
                {authLoading
                  ? 'Please wait...'
                  : authMode === 'login'
                    ? 'LOGIN TO DASHBOARD'
                    : 'CREATE ACCOUNT'}
              </button>
            </form>
          </section>
        </main>
      </div>
    )
  }

  return (
    <div className="app-shell">
      <div className="app-background">
        <div className="bg-glow glow-1" />
        <div className="bg-glow glow-2" />
      </div>

      <header className="hero-panel dashboard-hero">
        <div>
          <p className="eyebrow">CyberShield AI</p>
          <h1>Welcome back, {user.full_name}</h1>
          <p className="hero-copy">
            Your account is active, your dashboard is unlocked, and your analysis tools are ready.
          </p>
        </div>

        <div className="hero-actions">
          <div className="hero-pill">{user.email}</div>
          <button className="button-secondary" onClick={handleLogout} type="button">
            Logout
          </button>
        </div>
      </header>

      <main className="content-grid">
        <section className="panel controls-panel">
          <div className="panel-heading">
            <span className="panel-badge">Input Studio</span>
            <h2>Threat parameters</h2>
            <p>Adjust the model inputs and inspect how the score shifts.</p>
          </div>

          <div className="control-group">
            <label htmlFor="url-input">Profile / URL</label>
            <input
              id="url-input"
              type="text"
              placeholder="Paste Profile URL (e.g. instagr.am/spy_user)"
              value={inputs.url}
              onChange={updateInput('url')}
              className="text-input"
            />
          </div>

          <div className="control-group">
            <div className="slider-label">
              <span>🧠 Behavior Risk</span>
              <span>{inputs.behavior}%</span>
            </div>
            <input className="range-input" type="range" min="0" max="100" value={inputs.behavior} onChange={updateInput('behavior')} />
          </div>

          <div className="control-group">
            <div className="slider-label">
              <span>💬 NLP/Text Risk</span>
              <span>{inputs.nlp}%</span>
            </div>
            <input className="range-input" type="range" min="0" max="100" value={inputs.nlp} onChange={updateInput('nlp')} />
          </div>

          <div className="control-group">
            <div className="slider-label">
              <span>🌐 Network Risk</span>
              <span>{inputs.network}%</span>
            </div>
            <input className="range-input" type="range" min="0" max="100" value={inputs.network} onChange={updateInput('network')} />
          </div>

          <button className="button-primary" onClick={analyzeData} type="button" disabled={loading}>
            {loading ? 'ANALYZING...' : 'RUN REAL-TIME ANALYSIS'}
          </button>
          <button className="button-secondary" onClick={simulateStalkerAttack}>
            DUALITY SIMULATION
          </button>
        </section>

        <section className="panel insights-panel">
          <div className="panel-heading">
            <span className="panel-badge">Live insights</span>
            <h2>Behavior spikes</h2>
            <p>Watch threat activity react immediately as you tweak the controls.</p>
          </div>

          <div className="chart-card">
            <ResponsiveContainer width="100%" height={270}>
              <LineChart data={chartData} margin={{ top: 10, right: 10, left: -12, bottom: 0 }}>
                <CartesianGrid strokeDasharray="4 4" stroke="rgba(255,255,255,0.12)" />
                <XAxis dataKey="time" stroke="rgba(255,255,255,0.65)" tickLine={false} axisLine={false} />
                <YAxis stroke="rgba(255,255,255,0.65)" tickLine={false} axisLine={false} />
                <Tooltip contentStyle={{ background: '#0f172a', border: '1px solid rgba(148,163,184,0.2)', borderRadius: '14px', color: '#fff' }} cursor={{ stroke: 'rgba(99,102,241,0.4)', strokeWidth: 2 }} />
                <Line type="monotone" dataKey="activity" stroke="#818cf8" strokeWidth={4} dot={{ r: 3 }} activeDot={{ r: 6, strokeWidth: 3, stroke: '#e2e8f0' }} />
              </LineChart>
            </ResponsiveContainer>
          </div>

          {result ? (
            <div className={`results-card ${result.score > 70 ? 'alert' : 'safe'}`}>
              <div className="result-header">
                <div>
                  <p className="result-label">Threat score</p>
                  <h3>{result.score}%</h3>
                </div>
                <span className="status-pill">{result.status}</span>
              </div>
              <p className="result-copy">
                <strong>Reasoning:</strong> {result.reasons.join(', ')}
              </p>
              
              {result.ai_powered && result.ai_analysis && (
                <div className="ai-insights-box">
                  <p className="ai-badge">🤖 AI-Powered Analysis</p>
                  <div className="ai-detail">
                    <strong>Risk Level:</strong> {result.ai_analysis.overall_risk_level?.toUpperCase() || 'N/A'}
                  </div>
                  <div className="ai-detail">
                    <strong>AI Risk Score:</strong> {result.ai_analysis.risk_score || result.score}%
                  </div>
                  {result.ai_analysis.threat_indicators && result.ai_analysis.threat_indicators.length > 0 && (
                    <div className="ai-detail">
                      <strong>Indicators:</strong> {result.ai_analysis.threat_indicators.join(', ')}
                    </div>
                  )}
                </div>
              )}

              {result.score > 70 && <div className="alert-banner">High-risk alert forwarded to n8n</div>}
              {result.score > 70 && <div className="alert-banner">🚨 n8n alert sent to victim</div>}
            </div>
          ) : (
            <div className="results-card placeholder">
              <p>Analyze data to reveal the risk summary and visual alerts.</p>
            </div>
          )}
        </section>

        <section className="panel ai-recommendations-panel">
          <div className="panel-heading">
            <span className="panel-badge">AI Recommendations</span>
            <h2>Security Actions</h2>
            <p>AI-powered recommendations to mitigate risks.</p>
          </div>

          {aiRecommendations ? (
            <div className="recommendations-box">
              {aiRecommendations.immediate_actions && aiRecommendations.immediate_actions.length > 0 && (
                <div className="recommendation-section">
                  <h4>⚡ Immediate Actions</h4>
                  <ul>
                    {aiRecommendations.immediate_actions.map((action, idx) => (
                      <li key={idx}>{action}</li>
                    ))}
                  </ul>
                </div>
              )}

              {aiRecommendations.preventive_measures && aiRecommendations.preventive_measures.length > 0 && (
                <div className="recommendation-section">
                  <h4>🛡️ Preventive Measures</h4>
                  <ul>
                    {aiRecommendations.preventive_measures.map((measure, idx) => (
                      <li key={idx}>{measure}</li>
                    ))}
                  </ul>
                </div>
              )}

              {aiRecommendations.monitoring_suggestions && aiRecommendations.monitoring_suggestions.length > 0 && (
                <div className="recommendation-section">
                  <h4>👁️ Monitoring Suggestions</h4>
                  <ul>
                    {aiRecommendations.monitoring_suggestions.map((suggestion, idx) => (
                      <li key={idx}>{suggestion}</li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          ) : (
            <div className="results-card placeholder">
              <p>Run analysis to get AI recommendations.</p>
            </div>
          )}
        </section>

        {urlAssessment && (
          <section className="panel url-assessment-panel">
            <div className="panel-heading">
              <span className="panel-badge">URL Assessment</span>
              <h2>Domain Safety</h2>
              <p>AI analysis of the provided URL.</p>
            </div>

            <div className="url-assessment-box">
              <div className="safety-score">
                <span className="score-label">Safety Score</span>
                <div className="score-bar">
                  <div 
                    className={`score-fill ${urlAssessment.risk_level === 'safe' ? 'safe' : urlAssessment.risk_level === 'warning' ? 'warning' : 'dangerous'}`}
                    style={{ width: `${urlAssessment.safety_score || 0}%` }}
                  />
                </div>
                <span className="score-value">{urlAssessment.safety_score || 0}/100</span>
              </div>

              {urlAssessment.concerns && urlAssessment.concerns.length > 0 && (
                <div className="assessment-section">
                  <h4>⚠️ Concerns</h4>
                  <ul>
                    {urlAssessment.concerns.map((concern, idx) => (
                      <li key={idx}>{concern}</li>
                    ))}
                  </ul>
                </div>
              )}

              {urlAssessment.recommendations && urlAssessment.recommendations.length > 0 && (
                <div className="assessment-section">
                  <h4>Recommendations</h4>
                  <ul>
                    {urlAssessment.recommendations.map((rec, idx) => (
                      <li key={idx}>{rec}</li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          </section>
        )}
      </main>

      <section className="dashboard-footer">
        <div className="panel activity-log-panel">
          <div className="panel-heading">
            <span className="panel-badge">Activity log</span>
            <h2>Recent events</h2>
            <p>Latest security activities and alerts.</p>
          </div>
          <ul className="activity-list">
            {activityLog.map((item, index) => (
              <li key={index} className="activity-item">
                <span className="activity-time">{item.time}</span>
                <span className="activity-event">{item.event}</span>
              </li>
            ))}
          </ul>
        </div>

        <div className="panel weekly-analysis-panel">
          <div className="panel-heading">
            <span className="panel-badge">Weekly analysis</span>
            <h2>Threat distribution</h2>
            <p>Overview of risk levels this week.</p>
          </div>
          <div className="pie-chart-container">
            <ResponsiveContainer width="100%" height={200}>
              <PieChart>
                <Pie
                  data={pieData}
                  cx="50%"
                  cy="50%"
                  outerRadius={60}
                  fill="#8884d8"
                  dataKey="value"
                  label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                >
                  {pieData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>
      </section>
    </div>
  )
}

export default App
