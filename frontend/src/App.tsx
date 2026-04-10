import React, { useState, useEffect } from 'react'
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import Navbar from './components/Navbar'
import Home from './pages/Home'
import Books from './pages/Books'
import Reservations from './pages/Reservations'
import Profile from './pages/Profile'
import Statistics from './pages/Statistics'
import Calendar from './pages/Calendar'
import { getCurrentUser } from './api'
import { User } from './types'
import i18n from './i18n'
import './index.css'

function App() {
  const [user, setUser] = useState<User | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const token = localStorage.getItem('token')
    
    if (token) {
      getCurrentUser()
        .then(response => {
          setUser(response.data)
        })
        .catch(() => {
          localStorage.removeItem('token')
          localStorage.removeItem('refreshToken')
        })
        .finally(() => setLoading(false))
    } else {
      setLoading(false)
    }
  }, [])

  const login = (token: string) => {
    localStorage.setItem('token', token)
    getCurrentUser().then(response => {
      setUser(response.data)
    })
  }

  const logout = () => {
    const refreshToken = localStorage.getItem('refreshToken')
    if (refreshToken) {
      // Можно отправить запрос на logout
    }
    localStorage.removeItem('token')
    localStorage.removeItem('refreshToken')
    setUser(null)
  }

  if (loading) {
    return (
      <div className="loading">
        <div>{i18n.t('loading')}</div>
        <div className="loading-spinner"></div>
      </div>
    )
  }

  return (
    <Router>
      <div className="app">
        <Navbar user={user} onLogout={logout} />
        <main className="main-content">
          <Routes>
            <Route path="/" element={<Home user={user} onLogin={login} />} />
            <Route
              path="/books"
              element={user ? <Books /> : <Navigate to="/" />}
            />
            <Route
              path="/reservations"
              element={user ? <Reservations /> : <Navigate to="/" />}
            />
            <Route
              path="/profile"
              element={user ? <Profile user={user} /> : <Navigate to="/" />}
            />
            <Route
              path="/statistics"
              element={user ? <Statistics /> : <Navigate to="/" />}
            />
            <Route
              path="/calendar"
              element={user ? <Calendar /> : <Navigate to="/" />}
            />
          </Routes>
        </main>
      </div>
    </Router>
  )
}

export default App
