import React, { useState, useContext } from 'react'
import { Link } from 'react-router-dom'
import { AuthContext } from '../../context/AuthContext'

export default function Login(){
  const { login } = useContext(AuthContext)
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  async function handleSubmit(e){
    e.preventDefault()
    setError('')
    setLoading(true)
    try {
      // login() authenticates against POST /auth/login, then navigates by role.
      await login({ email, password })
    } catch (err) {
      const detail = err?.response?.data?.detail
      setError(typeof detail === 'string' ? detail : 'Invalid email or password.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-slate-950 py-12 px-4">
      <div className="max-w-md w-full">
        <div className="bg-black p-8 rounded-lg shadow-lg login-box">
          <div className="text-center mb-6">
            <h1 className="text-4xl font-bold text-yellow-400">Login</h1>
          </div>

          {error && (
            <div className="mb-4 p-3 bg-red-100 border border-red-400 text-red-700 rounded">
              {error}
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <label className="block text-sm font-medium text-yellow-400 mb-2">Email</label>
              <div className="bg-yellow-400 p-3 rounded-lg">
                <input
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  required
                  className="w-full bg-yellow-400 text-black placeholder-gray-600 outline-none font-medium"
                  placeholder="Enter your email"
                />
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-yellow-400 mb-2">Password</label>
              <div className="bg-yellow-400 p-3 rounded-lg">
                <input
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                  className="w-full bg-yellow-400 text-black placeholder-gray-600 outline-none font-medium"
                  placeholder="Enter your password"
                />
              </div>
            </div>

            <div className="flex items-center justify-between">
              <label className="flex items-center">
                <input type="checkbox" className="h-4 w-4 text-yellow-400 rounded border-yellow-300" />
                <span className="ml-2 text-sm text-yellow-300">Remember me</span>
              </label>
              <a href="#" className="text-sm text-yellow-400 hover:text-yellow-300 font-medium hover:underline">
                Forgot password?
              </a>
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full py-2 px-4 bg-yellow-400 text-black font-semibold rounded-lg hover:bg-yellow-300 transition disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? 'Signing in...' : 'Sign In'}
            </button>
          </form>

          <div className="mt-6 text-center">
            <p className="text-yellow-300 text-sm">
              Don't have an account?{' '}
              <Link to="/signup" className="text-yellow-400 hover:text-yellow-200 font-medium hover:underline">
                Sign up
              </Link>
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}
