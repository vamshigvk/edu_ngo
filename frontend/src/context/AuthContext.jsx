import React, { createContext, useState, useEffect, useRef } from 'react'
import api from '../services/api'
import { useNavigate } from 'react-router-dom'

export const AuthContext = createContext()

// Where each role lands after authenticating.
const HOME_FOR_ROLE = {
  admin: '/admin',
  mentor: '/mentor',
  mentee: '/mentee',
  reviewer: '/review',
}

// Decode a JWT payload without verifying (we only need `exp` client-side).
function readTokenExp(token) {
  try {
    const [, payload] = token.split('.')
    const json = JSON.parse(atob(payload.replace(/-/g, '+').replace(/_/g, '/')))
    return typeof json.exp === 'number' ? json.exp * 1000 : null // → ms epoch
  } catch {
    return null
  }
}

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)
  const navigate = useNavigate()
  const logoutTimer = useRef(null)

  function clearSession() {
    localStorage.removeItem('access_token')
    localStorage.removeItem('user')
    if (logoutTimer.current) clearTimeout(logoutTimer.current)
    setUser(null)
  }

  // Auto-logout exactly when the 1-hour token expires (so the user is dropped
  // even if they never make another request).
  function scheduleExpiry(token) {
    if (logoutTimer.current) clearTimeout(logoutTimer.current)
    const expMs = readTokenExp(token)
    if (!expMs) return
    const delay = expMs - Date.now()
    if (delay <= 0) {
      clearSession()
      return
    }
    logoutTimer.current = setTimeout(() => {
      clearSession()
      navigate('/login')
    }, delay)
  }

  // Restore a previously authenticated user from localStorage on load. The
  // session survives a page refresh; only an expired/absent token drops it.
  useEffect(() => {
    const token = localStorage.getItem('access_token')
    const stored = localStorage.getItem('user')
    const expMs = token ? readTokenExp(token) : null
    if (token && stored && expMs && expMs > Date.now()) {
      try {
        setUser(JSON.parse(stored))
        scheduleExpiry(token)
      } catch {
        clearSession()
      }
    } else if (token || stored) {
      clearSession()
    }
    setLoading(false)
    return () => {
      if (logoutTimer.current) clearTimeout(logoutTimer.current)
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
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
    const token = tokenRes.data.access_token
    localStorage.setItem('access_token', token)

    // The token response has no user payload — fetch the profile separately.
    const meRes = await api.get('/auth/me')
    const me = meRes.data
    localStorage.setItem('user', JSON.stringify(me))
    setUser(me)
    scheduleExpiry(token)

    navigate(HOME_FOR_ROLE[me.role] || '/')
    return me
  }

  const logout = () => {
    clearSession()
    navigate('/')
  }

  // Sign the onboarding declaration and refresh the cached user.
  const signDeclaration = async () => {
    const { data } = await api.post('/auth/declaration')
    localStorage.setItem('user', JSON.stringify(data))
    setUser(data)
    return data
  }

  return (
    <AuthContext.Provider value={{ user, loading, login, logout, signDeclaration }}>
      {children}
    </AuthContext.Provider>
  )
}
