import React from 'react'
import { Routes, Route } from 'react-router-dom'
import NavBar from './components/NavBar.jsx'
import Dashboard from './pages/Dashboard.jsx'
import Leaderboard from './pages/Leaderboard.jsx'
import EvaluatePage from './pages/EvaluatePage.jsx'
import ModelDetail from './pages/ModelDetail.jsx'

const styles = {
  app: { minHeight: '100vh', display: 'flex', flexDirection: 'column' },
  main: { flex: 1, padding: '24px', maxWidth: '1200px', margin: '0 auto', width: '100%' },
}

export default function App() {
  return (
    <div style={styles.app}>
      <NavBar />
      <main style={styles.main}>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/leaderboard" element={<Leaderboard />} />
          <Route path="/evaluate" element={<EvaluatePage />} />
          <Route path="/models/:id" element={<ModelDetail />} />
        </Routes>
      </main>
    </div>
  )
}

