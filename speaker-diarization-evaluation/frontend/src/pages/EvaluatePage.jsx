import React, { useEffect, useState } from 'react'
import { getModels, createModel, getRecordings, createRecording, createEvaluation } from '../services/api.js'
import StatusBadge from '../components/StatusBadge.jsx'

const s = {
  title: { fontSize: '1.6rem', fontWeight: 700, marginBottom: '8px' },
  sub: { color: '#64748b', marginBottom: '28px' },
  card: { background: '#fff', borderRadius: '12px', padding: '28px', boxShadow: '0 1px 4px rgba(0,0,0,0.08)', marginBottom: '24px', maxWidth: '700px' },
  sectionTitle: { fontSize: '1.05rem', fontWeight: 700, marginBottom: '18px', color: '#1e293b', borderBottom: '1px solid #e2e8f0', paddingBottom: '8px' },
  row: { display: 'flex', flexDirection: 'column', gap: '6px', marginBottom: '14px' },
  label: { fontSize: '0.82rem', fontWeight: 600, color: '#475569' },
  input: { padding: '8px 12px', borderRadius: '6px', border: '1px solid #cbd5e1', fontSize: '0.9rem', width: '100%' },
  select: { padding: '8px 12px', borderRadius: '6px', border: '1px solid #cbd5e1', fontSize: '0.9rem', width: '100%', background: '#fff' },
  btn: { padding: '10px 24px', background: '#2563eb', color: '#fff', border: 'none', borderRadius: '8px', fontWeight: 600, fontSize: '0.95rem', cursor: 'pointer' },
  resultCard: { background: '#f0fdf4', border: '1px solid #86efac', borderRadius: '10px', padding: '20px', marginTop: '20px' },
  errorCard: { background: '#fef2f2', border: '1px solid #fca5a5', borderRadius: '10px', padding: '20px', marginTop: '20px' },
  metricRow: { display: 'flex', gap: '24px', flexWrap: 'wrap', marginTop: '12px' },
  metric: { textAlign: 'center' },
  metricVal: { fontSize: '1.5rem', fontWeight: 800, color: '#166534' },
  metricLbl: { fontSize: '0.78rem', color: '#475569', fontWeight: 600 },
  tabs: { display: 'flex', gap: '0', marginBottom: '20px', borderRadius: '8px', overflow: 'hidden', border: '1px solid #e2e8f0' },
  tab: { flex: 1, padding: '10px', border: 'none', cursor: 'pointer', fontSize: '0.88rem', fontWeight: 600 },
}

const EMPTY_MODEL = { name: '', provider: '', version: '', model_type: 'open_source', run_method: 'local', description: '' }
const EMPTY_REC = { filename: '', num_speakers: '', condition: 'clean', reference_rttm_path: '', duration_seconds: '' }

export default function EvaluatePage() {
  const [models, setModels] = useState([])
  const [recordings, setRecordings] = useState([])
  const [modelTab, setModelTab] = useState('select') // 'select' | 'create'
  const [recTab, setRecTab] = useState('select')
  const [selectedModelId, setSelectedModelId] = useState('')
  const [selectedRecId, setSelectedRecId] = useState('')
  const [newModel, setNewModel] = useState(EMPTY_MODEL)
  const [newRec, setNewRec] = useState(EMPTY_REC)
  const [collar, setCollar] = useState(0.25)
  const [scoreOverlap, setScoreOverlap] = useState(true)
  const [file, setFile] = useState(null)
  const [result, setResult] = useState(null)
  const [error, setError] = useState('')
  const [submitting, setSubmitting] = useState(false)

  useEffect(() => {
    getModels().then(r => setModels(r.data)).catch(console.error)
    getRecordings().then(r => setRecordings(r.data)).catch(console.error)
  }, [])

  const handleCreateModel = async () => {
    try {
      const r = await createModel(newModel)
      setModels(prev => [r.data, ...prev])
      setSelectedModelId(r.data.id)
      setModelTab('select')
      setNewModel(EMPTY_MODEL)
    } catch (e) { alert('Failed to create model: ' + (e.response?.data?.detail || e.message)) }
  }

  const handleCreateRec = async () => {
    try {
      const payload = { ...newRec, num_speakers: newRec.num_speakers ? parseInt(newRec.num_speakers) : null, duration_seconds: newRec.duration_seconds ? parseFloat(newRec.duration_seconds) : null }
      const r = await createRecording(payload)
      setRecordings(prev => [r.data, ...prev])
      setSelectedRecId(r.data.id)
      setRecTab('select')
      setNewRec(EMPTY_REC)
    } catch (e) { alert('Failed to create recording: ' + (e.response?.data?.detail || e.message)) }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setResult(null)
    if (!selectedModelId) return setError('Please select or create a model.')
    if (!selectedRecId) return setError('Please select or create a recording.')
    if (!file) return setError('Please upload a hypothesis RTTM file.')

    const fd = new FormData()
    fd.append('model_id', selectedModelId)
    fd.append('recording_id', selectedRecId)
    fd.append('collar', collar)
    fd.append('score_overlap', scoreOverlap)
    fd.append('hypothesis_rttm', file)

    setSubmitting(true)
    try {
      const r = await createEvaluation(fd)
      setResult(r.data)
    } catch (e) {
      setError(e.response?.data?.detail || e.message)
    } finally {
      setSubmitting(false)
    }
  }

  const Tab = ({ id, label, active, onClick }) => (
    <button style={{ ...s.tab, background: active ? '#2563eb' : '#f8fafc', color: active ? '#fff' : '#475569' }} onClick={() => onClick(id)}>{label}</button>
  )

  return (
    <div>
      <div style={s.title}>⚙️ Submit Evaluation</div>
      <div style={s.sub}>Upload a hypothesis RTTM file and score it against the reference annotation.</div>

      <form onSubmit={handleSubmit}>
        {/* Step 1: Model */}
        <div style={s.card}>
          <div style={s.sectionTitle}>Step 1: Select or Register a Model</div>
          <div style={s.tabs}>
            <Tab id="select" label="Select Existing" active={modelTab === 'select'} onClick={setModelTab} />
            <Tab id="create" label="Register New" active={modelTab === 'create'} onClick={setModelTab} />
          </div>
          {modelTab === 'select' ? (
            <div style={s.row}>
              <label style={s.label}>Model</label>
              <select style={s.select} value={selectedModelId} onChange={e => setSelectedModelId(e.target.value)}>
                <option value="">— Select a model —</option>
                {models.map(m => <option key={m.id} value={m.id}>{m.name} ({m.provider || 'unknown'}) v{m.version || '?'}</option>)}
              </select>
            </div>
          ) : (
            <>
              {[['name','Model Name','text'],['provider','Provider','text'],['version','Version','text'],['run_method','Run Method','text'],['description','Description','text']].map(([k,l,t]) => (
                <div key={k} style={s.row}>
                  <label style={s.label}>{l}</label>
                  <input style={s.input} type={t} value={newModel[k]} onChange={e => setNewModel(p => ({...p, [k]: e.target.value}))} />
                </div>
              ))}
              <div style={s.row}>
                <label style={s.label}>Type</label>
                <select style={s.select} value={newModel.model_type} onChange={e => setNewModel(p => ({...p, model_type: e.target.value}))}>
                  <option value="open_source">Open Source</option>
                  <option value="commercial">Commercial</option>
                  <option value="api">API</option>
                </select>
              </div>
              <button type="button" style={s.btn} onClick={handleCreateModel}>Register Model</button>
            </>
          )}
        </div>

        {/* Step 2: Recording */}
        <div style={s.card}>
          <div style={s.sectionTitle}>Step 2: Select or Register a Recording</div>
          <div style={s.tabs}>
            <Tab id="select" label="Select Existing" active={recTab === 'select'} onClick={setRecTab} />
            <Tab id="create" label="Register New" active={recTab === 'create'} onClick={setRecTab} />
          </div>
          {recTab === 'select' ? (
            <div style={s.row}>
              <label style={s.label}>Recording</label>
              <select style={s.select} value={selectedRecId} onChange={e => setSelectedRecId(e.target.value)}>
                <option value="">— Select a recording —</option>
                {recordings.map(r => <option key={r.id} value={r.id}>{r.filename} ({r.condition || 'unknown'}, {r.num_speakers ?? '?'} spk)</option>)}
              </select>
            </div>
          ) : (
            <>
              {[['filename','Audio Filename'],['reference_rttm_path','Reference RTTM Path'],['duration_seconds','Duration (seconds)'],['num_speakers','Number of Speakers']].map(([k,l]) => (
                <div key={k} style={s.row}>
                  <label style={s.label}>{l}</label>
                  <input style={s.input} value={newRec[k]} onChange={e => setNewRec(p => ({...p, [k]: e.target.value}))} />
                </div>
              ))}
              <div style={s.row}>
                <label style={s.label}>Condition</label>
                <select style={s.select} value={newRec.condition} onChange={e => setNewRec(p => ({...p, condition: e.target.value}))}>
                  <option value="clean">Clean</option>
                  <option value="noisy">Noisy</option>
                  <option value="overlapping">Overlapping</option>
                </select>
              </div>
              <button type="button" style={s.btn} onClick={handleCreateRec}>Register Recording</button>
            </>
          )}
        </div>

        {/* Step 3: Upload + Settings */}
        <div style={s.card}>
          <div style={s.sectionTitle}>Step 3: Upload Hypothesis RTTM & Scoring Settings</div>
          <div style={s.row}>
            <label style={s.label}>Hypothesis RTTM File</label>
            <input type="file" accept=".rttm" onChange={e => setFile(e.target.files[0])} style={{ fontSize: '0.88rem' }} />
          </div>
          <div style={{ display: 'flex', gap: '24px', flexWrap: 'wrap' }}>
            <div style={s.row}>
              <label style={s.label}>Collar (seconds)</label>
              <input style={{ ...s.input, width: '100px' }} type="number" step="0.05" min="0" value={collar} onChange={e => setCollar(parseFloat(e.target.value))} />
            </div>
            <div style={{ ...s.row, flexDirection: 'row', alignItems: 'center', gap: '10px' }}>
              <input type="checkbox" id="overlap" checked={scoreOverlap} onChange={e => setScoreOverlap(e.target.checked)} />
              <label htmlFor="overlap" style={s.label}>Score Overlapping Speech</label>
            </div>
          </div>
        </div>

        {error && <div style={s.errorCard}><strong>Error:</strong> {error}</div>}

        <button type="submit" style={{ ...s.btn, fontSize: '1rem', padding: '12px 36px' }} disabled={submitting}>
          {submitting ? 'Scoring…' : '🚀 Run Evaluation'}
        </button>
      </form>

      {result && (
        <div style={s.resultCard}>
          <strong>✅ Evaluation Complete</strong> — <StatusBadge status={result.status} />
          {result.status === 'completed' && (
            <div style={s.metricRow}>
              {[['DER', result.der],['JER', result.jer],['Miss', result.miss_rate],['False Alarm', result.false_alarm_rate],['Confusion', result.confusion_rate]].map(([l,v]) => (
                <div key={l} style={s.metric}>
                  <div style={s.metricVal}>{v != null ? `${v.toFixed(2)}%` : '—'}</div>
                  <div style={s.metricLbl}>{l}</div>
                </div>
              ))}
              <div style={s.metric}>
                <div style={{ ...s.metricVal, color: '#1e40af' }}>{result.runtime_seconds?.toFixed(2)}s</div>
                <div style={s.metricLbl}>Runtime</div>
              </div>
            </div>
          )}
          {result.error_message && <p style={{ color: '#991b1b', marginTop: '10px' }}>{result.error_message}</p>}
        </div>
      )}
    </div>
  )
}

