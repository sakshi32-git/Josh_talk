import React from 'react'
import { Link, useLocation } from 'react-router-dom'

const links = [
  { to: '/', label: 'Dashboard' },
  { to: '/leaderboard', label: 'Leaderboard' },
  { to: '/evaluate', label: 'Evaluate' },
]

const styles = {
  nav: {
    background: '#1e293b',
    color: '#fff',
    padding: '0 24px',
    display: 'flex',
    alignItems: 'center',
    gap: '32px',
    height: '56px',
    boxShadow: '0 2px 8px rgba(0,0,0,0.2)',
  },
  brand: { fontSize: '1.2rem', fontWeight: 700, color: '#fff', textDecoration: 'none' },
  link: { color: '#94a3b8', textDecoration: 'none', fontSize: '0.95rem', fontWeight: 500, padding: '4px 0' },
  activeLink: { color: '#38bdf8', borderBottom: '2px solid #38bdf8' },
}

export default function NavBar() {
  const { pathname } = useLocation()
  return (
    <nav style={styles.nav}>
      <Link to="/" style={styles.brand}>🎙️ Diarization Leaderboard</Link>
      {links.map(({ to, label }) => (
        <Link
          key={to}
          to={to}
          style={{ ...styles.link, ...(pathname === to ? styles.activeLink : {}) }}
        >
          {label}
        </Link>
      ))}
    </nav>
  )
}

