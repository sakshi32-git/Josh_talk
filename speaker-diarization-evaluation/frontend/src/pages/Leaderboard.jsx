import React, { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer,
} from 'recharts'
import { getLeaderboard } from '../services/api.js'

const derColor = (der) => {
  if (der == null) return '#94a3b8'
  if (der < 15) return '#16a34a'
  if (der < 30) return '#d97706'
  return '#dc2626'
}

const s = {
  title: { fontSize: '1.6rem', fontWeight: 700, marginBottom: '8px' },
  sub: { color: '#64748b', marginBottom: '20px' },
  filters: { display: 'flex', gap: '12px', marginBottom: '20px', flexWrap: 'wrap', alignItems: 'center' },
  filterLabel: { fontSize: '0.85rem', fontWeight: 600, color: '#475569' },
  select: { padding: '6px 10px', borderRadius: '6px', border: '1px solid #cbd5e1', fontSize: '0.85rem' },
  input: { padding: '6px 10px', borderRadius: '6px', border: '1px solid #cbd5e1', width: '70px', fontSize: '0.85rem' },
  card: { background: '#fff', borderRadius: '12px', padding: '24px', boxShadow: '0 1px 4px rgba(0,0,0,0.08)', marginBottom: '24px' },
  table: { width: '100%', borderCollapse: 'collapse', fontSize: '0.88rem' },
  th: { textAlign: 'left', padding: '10px 12px', background: '#f8fafc', fontWeight: 600, borderBottom: '2px solid #e2e8f0', color: '#475569', whiteSpace: 'nowrap' },
  td: { padding: '10px 12px', borderBottom: '1px solid #f1f5f9' },
  rank: { fontWeight: 700, color: '#475569', textAlign: 'center' },
}

export default function Leaderboard() {
  const [entries, setEntries] = useState([])
  const [loading, setLoading] = useState(true)
  const [condition, setCondition] = useState('')
  const [minSpeakers, setMinSpeakers] = useState('')
  const [maxSpeakers, setMaxSpeakers] = useState('')

  const fetchData = () => {
    setLoading(true)
    const params = {}
    if (condition) params.condition = condition
    if (minSpeakers) params.min_speakers = minSpeakers
    if (maxSpeakers) params.max_speakers = maxSpeakers
    getLeaderboard(params)
      .then(r => setEntries(r.data))
      .catch(console.error)
      .finally(() => setLoading(false))
  }

  useEffect(() => { fetchData() }, [condition, minSpeakers, maxSpeakers])

  const chartData = entries
    .filter(e => e.avg_der != null)
    .map(e => ({ name: e.model_name, DER: e.avg_der, JER: e.avg_jer }))

  return (
    <div>
      <div style={s.title}>🏆 Leaderboard</div>
      <div style={s.sub}>Models ranked by average DER (lower is better). Failed runs are excluded from rankings.</div>

      <div style={s.filters}>
        <span style={s.filterLabel}>Filters:</span>
        <select style={s.select} value={condition} onChange={e => setCondition(e.target.value)}>
          <option value="">All Conditions</option>
          <option value="clean">Clean</option>
          <option value="noisy">Noisy</option>
          <option value="overlapping">Overlapping</option>
        </select>
        <span style={s.filterLabel}>Speakers:</span>
        <input style={s.input} type="number" placeholder="Min" value={minSpeakers} onChange={e => setMinSpeakers(e.target.value)} min="1" />
        <span style={{ color: '#94a3b8' }}>–</span>
        <input style={s.input} type="number" placeholder="Max" value={maxSpeakers} onChange={e => setMaxSpeakers(e.target.value)} min="1" />
      </div>

      {loading ? <p>Loading…</p> : (
        <>
          {chartData.length > 0 && (
            <div style={s.card}>
              <div style={{ fontWeight: 700, marginBottom: '16px' }}>DER / JER by Model</div>
              <ResponsiveContainer width="100%" height={260}>
                <BarChart data={chartData} margin={{ top: 5, right: 20, left: 0, bottom: 5 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
                  <XAxis dataKey="name" tick={{ fontSize: 11 }} />
                  <YAxis unit="%" tick={{ fontSize: 11 }} />
                  <Tooltip formatter={(v) => `${v?.toFixed(2)}%`} />
                  <Legend />
                  <Bar dataKey="DER" fill="#3b82f6" radius={[4, 4, 0, 0]} />
                  <Bar dataKey="JER" fill="#f59e0b" radius={[4, 4, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </div>
          )}

          <div style={s.card}>
            {entries.length === 0 ? (
              <p style={{ color: '#94a3b8' }}>No results yet. Submit evaluations to populate the leaderboard.</p>
            ) : (
              <table style={s.table}>
                <thead>
                  <tr>
                    <th style={{ ...s.th, textAlign: 'center' }}>Rank</th>
                    <th style={s.th}>Model</th>
                    <th style={s.th}>Provider</th>
                    <th style={s.th}>Version</th>
                    <th style={s.th}>DER (%)</th>
                    <th style={s.th}>JER (%)</th>
                    <th style={s.th}>Miss (%)</th>
                    <th style={s.th}>FA (%)</th>
                    <th style={s.th}>Confusion (%)</th>
                    <th style={s.th}># Recs</th>
                    <th style={s.th}># Failed</th>
                    <th style={s.th}>Avg RT (s)</th>
                  </tr>
                </thead>
                <tbody>
                  {entries.map((e, i) => (
                    <tr key={e.model_id} style={{ background: i % 2 === 0 ? '#fff' : '#f8fafc' }}>
                      <td style={{ ...s.td, ...s.rank }}>{i + 1}</td>
                      <td style={s.td}>
                        <Link to={`/models/${e.model_id}`} style={{ color: '#2563eb', fontWeight: 600, textDecoration: 'none' }}>
                          {e.model_name}
                        </Link>
                      </td>
                      <td style={s.td}>{e.provider || '—'}</td>
                      <td style={s.td}>{e.version || '—'}</td>
                      <td style={{ ...s.td, fontWeight: 700, color: derColor(e.avg_der) }}>
                        {e.avg_der != null ? `${e.avg_der.toFixed(2)}%` : '—'}
                      </td>
                      <td style={s.td}>{e.avg_jer != null ? `${e.avg_jer.toFixed(2)}%` : '—'}</td>
                      <td style={s.td}>{e.avg_miss != null ? `${e.avg_miss.toFixed(2)}%` : '—'}</td>
                      <td style={s.td}>{e.avg_false_alarm != null ? `${e.avg_false_alarm.toFixed(2)}%` : '—'}</td>
                      <td style={s.td}>{e.avg_confusion != null ? `${e.avg_confusion.toFixed(2)}%` : '—'}</td>
                      <td style={s.td}>{e.num_recordings}</td>
                      <td style={{ ...s.td, color: e.num_failed > 0 ? '#dc2626' : '#16a34a', fontWeight: e.num_failed > 0 ? 700 : 400 }}>
                        {e.num_failed}
                      </td>
                      <td style={s.td}>{e.avg_runtime != null ? e.avg_runtime.toFixed(2) : '—'}</td>
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

