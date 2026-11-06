import React, { useEffect, useState } from 'react'
import { useParams, Link } from 'react-router-dom'
import { getModelById } from '../services/api.js'
import StatusBadge from '../components/StatusBadge.jsx'
import MetricCard from '../components/MetricCard.jsx'

const s = {
  back: { color: '#2563eb', textDecoration: 'none', fontSize: '0.9rem', display: 'inline-block', marginBottom: '16px' },
  title: { fontSize: '1.5rem', fontWeight: 700, marginBottom: '4px' },
  meta: { color: '#64748b', fontSize: '0.88rem', marginBottom: '24px' },
  cards: { display: 'flex', gap: '14px', flexWrap: 'wrap', marginBottom: '28px' },
  card: { background: '#fff', borderRadius: '12px', padding: '24px', boxShadow: '0 1px 4px rgba(0,0,0,0.08)', marginBottom: '24px' },
  sectionTitle: { fontSize: '1rem', fontWeight: 700, marginBottom: '14px', color: '#1e293b' },
  table: { width: '100%', borderCollapse: 'collapse', fontSize: '0.85rem' },
  th: { textAlign: 'left', padding: '8px 12px', background: '#f8fafc', fontWeight: 600, borderBottom: '1px solid #e2e8f0', color: '#475569' },
  td: { padding: '8px 12px', borderBottom: '1px solid #f1f5f9' },
  badge: { display: 'inline-block', padding: '2px 8px', borderRadius: '4px', fontSize: '0.75rem', fontWeight: 600, background: '#e0f2fe', color: '#0369a1' },
}

export default function ModelDetail() {
  const { id } = useParams()
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    getModelById(id)
      .then(r => setData(r.data))
      .catch(console.error)
      .finally(() => setLoading(false))
  }, [id])

  if (loading) return <p>Loading…</p>
  if (!data) return <p style={{ color: '#dc2626' }}>Model not found.</p>

  const { stats, evaluation_runs } = data

  return (
    <div>
      <Link to="/leaderboard" style={s.back}>← Back to Leaderboard</Link>
      <div style={s.title}>{data.name}</div>
      <div style={s.meta}>
        <span style={s.badge}>{data.model_type || 'unknown'}</span>{' '}
        {data.provider && <strong>{data.provider}</strong>}
        {data.version && ` · v${data.version}`}
        {data.run_method && ` · ${data.run_method}`}
      </div>
      {data.description && <p style={{ color: '#475569', marginBottom: '20px' }}>{data.description}</p>}

      <div style={s.cards}>
        <MetricCard label="Avg DER" value={stats.avg_der != null ? `${stats.avg_der.toFixed(2)}%` : '—'} color={stats.avg_der != null ? (stats.avg_der < 15 ? 'green' : stats.avg_der < 30 ? 'yellow' : 'red') : 'gray'} />
        <MetricCard label="Avg JER" value={stats.avg_jer != null ? `${stats.avg_jer.toFixed(2)}%` : '—'} color="blue" />
        <MetricCard label="Completed" value={stats.num_completed} color="green" />
        <MetricCard label="Failed" value={stats.num_failed} color={stats.num_failed > 0 ? 'red' : 'gray'} />
        <MetricCard label="Avg Runtime" value={stats.avg_runtime != null ? `${stats.avg_runtime.toFixed(2)}s` : '—'} color="gray" />
      </div>

      <div style={s.card}>
        <div style={s.sectionTitle}>Per-Recording Breakdown</div>
        {evaluation_runs.length === 0 ? (
          <p style={{ color: '#94a3b8' }}>No evaluation runs yet.</p>
        ) : (
          <table style={s.table}>
            <thead>
              <tr>
                <th style={s.th}>Recording ID</th>
                <th style={s.th}>Status</th>
                <th style={s.th}>DER (%)</th>
                <th style={s.th}>JER (%)</th>
                <th style={s.th}>Miss (%)</th>
                <th style={s.th}>FA (%)</th>
                <th style={s.th}>Confusion (%)</th>
                <th style={s.th}>Runtime (s)</th>
                <th style={s.th}>Date</th>
              </tr>
            </thead>
            <tbody>
              {evaluation_runs.map(r => (
                <tr key={r.run_id}>
                  <td style={s.td}><code style={{ fontSize: '0.78rem' }}>{r.recording_id.slice(0, 16)}…</code></td>
                  <td style={s.td}><StatusBadge status={r.status} /></td>
                  <td style={s.td}>{r.der != null ? r.der.toFixed(2) : '—'}</td>
                  <td style={s.td}>{r.jer != null ? r.jer.toFixed(2) : '—'}</td>
                  <td style={s.td}>{r.miss_rate != null ? r.miss_rate.toFixed(2) : '—'}</td>
                  <td style={s.td}>{r.false_alarm_rate != null ? r.false_alarm_rate.toFixed(2) : '—'}</td>
                  <td style={s.td}>{r.confusion_rate != null ? r.confusion_rate.toFixed(2) : '—'}</td>
                  <td style={s.td}>{r.runtime_seconds != null ? r.runtime_seconds.toFixed(2) : '—'}</td>
                  <td style={s.td}>{r.created_at ? new Date(r.created_at).toLocaleDateString() : '—'}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  )
}

