import React from 'react'

const statusConfig = {
  completed: { bg: '#dcfce7', color: '#166534', label: '✓ Completed' },
  failed: { bg: '#fee2e2', color: '#991b1b', label: '✗ Failed' },
  pending: { bg: '#fef9c3', color: '#854d0e', label: '⏳ Pending' },
  running: { bg: '#dbeafe', color: '#1e40af', label: '⚙ Running' },
  timed_out: { bg: '#f3e8ff', color: '#6b21a8', label: '⏱ Timed Out' },
}

export default function StatusBadge({ status }) {
  const cfg = statusConfig[status] || { bg: '#f1f5f9', color: '#475569', label: status }
  return (
    <span style={{
      background: cfg.bg,
      color: cfg.color,
      borderRadius: '999px',
      padding: '2px 10px',
      fontSize: '0.78rem',
      fontWeight: 600,
    }}>
      {cfg.label}
    </span>
  )
}

