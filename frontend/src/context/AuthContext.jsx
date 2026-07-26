import React, { createContext, useState, useEffect } from 'react'
import api from '../services/api'
import { useNavigate } from 'react-router-dom'

export const AuthContext = createContext()

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)
  const navigate = useNavigate()

  // Restore a previously authenticated user from localStorage on load.
  useEffect(() => {
    const stored = localStorage.getItem('user')
    if (stored) {
      try {
        setUser(JSON.parse(stored))
      } catch {
        localStorage.removeItem('user')
      }
    }
    setLoading(false)
  }, [])

  const login = async (credentials) => {
    // Backend uses the OAuth2 password flow: form-encoded body whose
    // `username` field carries the email. Response is { access_token, token_type }.
    const body = new URLSearchParams()
    body.append('username', credentials.email)
    body.append('password', credentials.password)

    const tokenRes = await api.post('/auth/login', body, {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    })
    localStorage.setItem('access_token', tokenRes.data.access_token)

    // The token response has no user payload — fetch the profile separately.
    const meRes = await api.get('/auth/me')
    const me = meRes.data
    localStorage.setItem('user', JSON.stringify(me))
    setUser(me)

    // Only the admin dashboard exists today; everyone else lands on home.
    if (me.role === 'admin') navigate('/admin')
    else navigate('/')
    return me
  }

  const logout = () => {
    localStorage.removeItem('access_token')
    localStorage.removeItem('user')
    setUser(null)
    navigate('/')
  }

  return (
    <AuthContext.Provider value={{ user, loading, login, logout }}>
      {children}
    </AuthContext.Provider>
  )
}
