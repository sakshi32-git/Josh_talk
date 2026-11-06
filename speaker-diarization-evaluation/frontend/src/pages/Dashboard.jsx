import React, { useEffect, useState } from 'react'
import { getLeaderboard, getEvaluations, getModels, getRecordings } from '../services/api.js'
import MetricCard from '../components/MetricCard.jsx'
import StatusBadge from '../components/StatusBadge.jsx'

const s = {
  title: { fontSize: '1.6rem', fontWeight: 700, marginBottom: '8px' },
  sub: { color: '#64748b', marginBottom: '28px' },
  cards: { display: 'flex', gap: '16px', flexWrap: 'wrap', marginBottom: '32px' },
  section: { background: '#fff', borderRadius: '12px', padding: '24px', boxShadow: '0 1px 4px rgba(0,0,0,0.08)', marginBottom: '24px' },
  sectionTitle: { fontSize: '1rem', fontWeight: 700, marginBottom: '16px', color: '#1e293b' },
  table: { width: '100%', borderCollapse: 'collapse', fontSize: '0.88rem' },
  th: { textAlign: 'left', padding: '8px 12px', background: '#f8fafc', fontWeight: 600, borderBottom: '1px solid #e2e8f0', color: '#475569' },
  td: { padding: '8px 12px', borderBottom: '1px solid #f1f5f9', color: '#374151' },
}

export default function Dashboard() {
  const [entries, setEntries] = useState([])
  const [runs, setRuns] = useState([])
  const [models, setModels] = useState([])
  const [recordings, setRecordings] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    Promise.all([getLeaderboard(), getEvaluations(), getModels(), getRecordings()])
      .then(([lb, ev, mo, rc]) => {
        setEntries(lb.data)
        setRuns(ev.data)
        setModels(mo.data)
        setRecordings(rc.data)
      })
      .catch(console.error)
      .finally(() => setLoading(false))
  }, [])

  const completed = runs.filter(r => r.status === 'completed').length
  const failed = runs.filter(r => r.status === 'failed').length

  return (
    <div>
      <div style={s.title}>📊 Dashboard</div>
      <div style={s.sub}>Overview of your speaker diarization evaluation platform.</div>

      {loading ? <p>Loading…</p> : (
        <>
          <div style={s.cards}>
            <MetricCard label="Models" value={models.length} color="blue" />
            <MetricCard label="Recordings" value={recordings.length} color="gray" />
            <MetricCard label="Completed Runs" value={completed} color="green" />
            <MetricCard label="Failed Runs" value={failed} color="red" />
          </div>

          <div style={s.section}>
            <div style={s.sectionTitle}>Recent Evaluation Runs</div>
            {runs.length === 0 ? (
              <p style={{ color: '#94a3b8' }}>No runs yet. Go to <strong>Evaluate</strong> to submit your first evaluation.</p>
            ) : (
              <table style={s.table}>
                <thead>
                  <tr>
                    <th style={s.th}>Run ID</th>
                    <th style={s.th}>Model</th>
                    <th style={s.th}>Recording</th>
                    <th style={s.th}>Status</th>
                    <th style={s.th}>DER (%)</th>
                    <th style={s.th}>JER (%)</th>
                    <th style={s.th}>Runtime (s)</th>
                  </tr>
                </thead>
                <tbody>
                  {runs.slice(0, 10).map(r => (
                    <tr key={r.id}>
                      <td style={s.td}><code style={{ fontSize: '0.78rem' }}>{r.id.slice(0, 8)}…</code></td>
                      <td style={s.td}>{r.model_id.slice(0, 8)}…</td>
                      <td style={s.td}>{r.recording_id.slice(0, 12)}…</td>
                      <td style={s.td}><StatusBadge status={r.status} /></td>
                      <td style={s.td}>{r.der != null ? r.der.toFixed(2) : '—'}</td>
                      <td style={s.td}>{r.jer != null ? r.jer.toFixed(2) : '—'}</td>
                      <td style={s.td}>{r.runtime_seconds != null ? r.runtime_seconds.toFixed(2) : '—'}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            )}
          </div>
        </>
      )}
    </div>
  )
}

