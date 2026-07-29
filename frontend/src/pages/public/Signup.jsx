import React, { useState, useContext } from 'react'
import { Link } from 'react-router-dom'
import api from '../../services/api'
import { AuthContext } from '../../context/AuthContext'

const EMPTY = { full_name: '', email: '', password: '', role: 'mentee' }

export default function Signup(){
  const { login } = useContext(AuthContext)
  const [form, setForm] = useState(EMPTY)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  function update(field){
    return (e) => setForm({ ...form, [field]: e.target.value })
  }

  async function handleSubmit(e){
    e.preventDefault()
    setError('')
    setLoading(true)
    try {
      // Create the account, then sign in immediately for a smooth hand-off.
      await api.post('/auth/register', form)
      await login({ email: form.email, password: form.password })
    } catch (err) {
      const detail = err?.response?.data?.error?.message || err?.response?.data?.detail
      setError(typeof detail === 'string' ? detail : 'Could not create your account.')
    } finally {
      setLoading(false)
    }
  }

  const fieldWrap = 'bg-yellow-400 p-3 rounded-lg'
  const fieldInput = 'w-full bg-yellow-400 text-black placeholder-gray-600 outline-none font-medium'

  return (
    <div className="min-h-screen flex items-center justify-center bg-slate-950 py-12 px-4">
      <div className="max-w-md w-full">
        <div className="bg-black p-8 rounded-lg shadow-lg">
          <div className="text-center mb-6">
            <h1 className="text-4xl font-bold text-yellow-400">Sign Up</h1>
          </div>

          {error && (
            <div className="mb-4 p-3 bg-red-100 border border-red-400 text-red-700 rounded">
              {error}
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-5">
            <div>
              <label className="block text-sm font-medium text-yellow-400 mb-2">Full name</label>
              <div className={fieldWrap}>
                <input value={form.full_name} onChange={update('full_name')} required className={fieldInput} placeholder="Your name" />
              </div>
            </div>
            <div>
              <label className="block text-sm font-medium text-yellow-400 mb-2">Email</label>
              <div className={fieldWrap}>
                <input type="email" value={form.email} onChange={update('email')} required className={fieldInput} placeholder="you@example.com" />
              </div>
            </div>
            <div>
              <label className="block text-sm font-medium text-yellow-400 mb-2">Password</label>
              <div className={fieldWrap}>
                <input type="password" value={form.password} onChange={update('password')} required minLength={6} className={fieldInput} placeholder="Choose a password" />
              </div>
            </div>
            <div>
              <label className="block text-sm font-medium text-yellow-400 mb-2">I am a</label>
              <div className={fieldWrap}>
                <select value={form.role} onChange={update('role')} className={`${fieldInput} cursor-pointer`}>
                  <option value="mentee">Mentee (student)</option>
                  <option value="mentor">Mentor</option>
                </select>
              </div>
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full py-2 px-4 bg-yellow-400 text-black font-semibold rounded-lg hover:bg-yellow-300 transition disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? 'Creating account...' : 'Create account'}
            </button>
          </form>

          <div className="mt-6 text-center">
            <p className="text-yellow-300 text-sm">
              Already have an account?{' '}
              <Link to="/login" className="text-yellow-400 hover:text-yellow-200 font-medium hover:underline">
                Log in
              </Link>
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}
