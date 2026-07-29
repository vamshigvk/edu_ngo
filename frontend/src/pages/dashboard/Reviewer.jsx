import React, { useContext, useEffect, useState } from 'react'
import api from '../../services/api'
import { AuthContext } from '../../context/AuthContext'

function errText(err, fallback){
  const detail = err?.response?.data?.error?.message || err?.response?.data?.detail
  return typeof detail === 'string' ? detail : fallback
}

function ReviewCard({ item, onSubmitted }){
  const [decision, setDecision] = useState(item.my_decision || 'select')
  const [description, setDescription] = useState(item.my_description || '')
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState('')

  async function submit(e){
    e.preventDefault()
    setSaving(true); setError('')
    try {
      await api.post(`/api/reviews/${item.review_id}/submit`, { decision, description })
      onSubmitted()
    } catch (err) {
      setError(errText(err, 'Could not submit your review.'))
    } finally { setSaving(false) }
  }

  return (
    <li className="p-4 bg-white rounded shadow-sm border">
      <div className="flex justify-between items-start gap-4">
        <div>
          <p className="font-semibold text-gray-900">{item.applicant_name || 'Applicant'}</p>
          <p className="text-sm text-gray-500">Disadvantage score: {item.disadvantage_score}</p>
        </div>
        {item.my_decision && (
          <span className="text-xs uppercase px-2 py-1 rounded bg-green-100 text-green-700">
            submitted: {item.my_decision}
          </span>
        )}
      </div>

      {Object.keys(item.answers || {}).length > 0 && (
        <dl className="mt-3 grid grid-cols-1 sm:grid-cols-2 gap-x-6 gap-y-1 text-sm">
          {Object.entries(item.answers).map(([k, v]) => (
            <div key={k} className="flex gap-2">
              <dt className="text-gray-500">{k}:</dt>
              <dd className="text-gray-800">{v == null || v === '' ? '—' : String(v)}</dd>
            </div>
          ))}
        </dl>
      )}

      {error && <div className="mt-3 p-2 bg-red-100 border border-red-400 text-red-700 rounded text-sm">{error}</div>}

      <form onSubmit={submit} className="mt-4 flex flex-col sm:flex-row gap-3 sm:items-end">
        <label className="text-sm text-gray-600">Decision
          <select value={decision} onChange={e => setDecision(e.target.value)} className="mt-1 block p-2 rounded border">
            <option value="select">Select</option>
            <option value="reject">Reject</option>
          </select>
        </label>
        <label className="text-sm text-gray-600 flex-1">Screening notes
          <input value={description} onChange={e => setDescription(e.target.value)} placeholder="Reviewer description" className="mt-1 block w-full p-2 rounded border" />
        </label>
        <button disabled={saving} className="px-4 py-2 bg-yellow-600 text-white rounded disabled:opacity-50">
          {saving ? 'Saving...' : 'Submit review'}
        </button>
      </form>
    </li>
  )
}

export default function Reviewer(){
  const { user, logout } = useContext(AuthContext)
  const [items, setItems] = useState([])
  const [error, setError] = useState('')

  async function load(){
    try {
      const { data } = await api.get('/api/reviews/assigned')
      setItems(data)
    } catch (err) {
      setError(errText(err, 'Could not load your assigned applications.'))
    }
  }
  useEffect(() => { load() }, [])

  return (
    <div className="max-w-4xl mx-auto px-4 py-10">
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Reviewer — Profile Screening</h1>
          <p className="text-gray-600 mt-1">Welcome, {user?.full_name}.</p>
        </div>
        <button onClick={logout} className="px-4 py-2 bg-black text-yellow-400 font-semibold rounded hover:bg-gray-900">Logout</button>
      </div>

      {error && <div className="mb-6 p-3 bg-red-100 border border-red-400 text-red-700 rounded">{error}</div>}

      {items.length === 0 ? (
        <p className="text-gray-600">No applications are assigned to you yet.</p>
      ) : (
        <ul className="space-y-4">
          {items.map(item => (
            <ReviewCard key={item.review_id} item={item} onSubmitted={load} />
          ))}
        </ul>
      )}
    </div>
  )
}
