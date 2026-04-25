import { useState } from 'react'
import axios from 'axios'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'
import './App.css'

function App() {
  const [inputs, setInputs] = useState({ behavior: 50, nlp: 50, network: 50, url: '' })
  const [result, setResult] = useState(null)

  const chartData = [
    { time: '10pm', activity: 22 },
    { time: '12am', activity: inputs.behavior > 60 ? 83 : 42 },
    { time: '02am', activity: inputs.behavior > 80 ? 97 : 53 },
    { time: '04am', activity: 31 },
  ]

  const analyzeData = async () => {
    try {
      const response = await axios.post('http://127.0.0.1:5000/analyze', {
        behavior_input: inputs.behavior,
        nlp_input: inputs.nlp,
        network_input: inputs.network,
        url: inputs.url,
      })
      setResult(response.data)
    } catch (error) {
      alert('Backend not connected. Please start python app.py and try again.')
    }
  }

  const updateInput = (key) => (event) => {
    const value = key === 'url' ? event.target.value : Number(event.target.value)
    setInputs({ ...inputs, [key]: value })
  }

  return (
    <div className="app-shell">
      <div className="app-background">
        <div className="bg-glow glow-1" />
        <div className="bg-glow glow-2" />
      </div>

      <header className="hero-panel">
        <div>
          <p className="eyebrow">CyberShield AI</p>
          <h1>Make your threat dashboard look premium</h1>
          <p className="hero-copy">
            Clean visuals, smooth motion, and a smart layout help your project present like a product.
          </p>
        </div>
        <div className="hero-pill">Realtime analysis · Threat scoring · Visual insights</div>
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

          <button className="button-primary" onClick={analyzeData}>
            RUN REAL-TIME ANALYSIS
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
              {result.score > 70 && <div className="alert-banner">🚨 n8n alert sent to victim</div>}
            </div>
          ) : (
            <div className="results-card placeholder">
              <p>Analyze data to reveal the risk summary and visual alerts.</p>
            </div>
          )}
        </section>
      </main>
    </div>
  )
}

export default App
