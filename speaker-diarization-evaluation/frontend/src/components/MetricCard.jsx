import React from 'react'

const colorMap = {
  green: { bg: '#dcfce7', border: '#86efac', text: '#166534' },
  yellow: { bg: '#fef9c3', border: '#fde047', text: '#854d0e' },
  red: { bg: '#fee2e2', border: '#fca5a5', text: '#991b1b' },
  blue: { bg: '#dbeafe', border: '#93c5fd', text: '#1e40af' },
  gray: { bg: '#f1f5f9', border: '#cbd5e1', text: '#475569' },
}

export default function MetricCard({ label, value, color = 'gray', subtitle }) {
  const c = colorMap[color] || colorMap.gray
  return (
    <div style={{
      background: c.bg,
      border: `1px solid ${c.border}`,
      borderRadius: '10px',
      padding: '20px 24px',
      minWidth: '150px',
      flex: 1,
    }}>
      <div style={{ fontSize: '0.8rem', fontWeight: 600, color: c.text, textTransform: 'uppercase', letterSpacing: '0.05em' }}>
        {label}
      </div>
      <div style={{ fontSize: '2rem', fontWeight: 800, color: c.text, margin: '6px 0' }}>
        {value ?? '—'}
      </div>
      {subtitle && <div style={{ fontSize: '0.78rem', color: c.text, opacity: 0.8 }}>{subtitle}</div>}
    </div>
  )
}

