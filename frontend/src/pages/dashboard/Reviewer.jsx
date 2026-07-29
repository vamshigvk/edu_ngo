import React, { useContext, useEffect, useState } from 'react'
import api from '../../services/api'
import { AuthContext } from '../../context/AuthContext'
import { PageHeader, Card, Badge, Button, ErrorBanner, EmptyState, inputClass } from '../../components/ui'

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
    <Card as="li" className="p-4">
      <div className="flex justify-between items-start gap-4">
        <div>
          <p className="font-semibold text-neutral-900">{item.applicant_name || 'Applicant'}</p>
          <p className="text-sm text-neutral-500">Disadvantage score: {item.disadvantage_score}</p>
        </div>
        {item.my_decision && <Badge tone="green">submitted: {item.my_decision}</Badge>}
      </div>

      {Object.keys(item.answers || {}).length > 0 && (
        <dl className="mt-3 grid grid-cols-1 sm:grid-cols-2 gap-x-6 gap-y-1 text-sm">
          {Object.entries(item.answers).map(([k, v]) => (
            <div key={k} className="flex gap-2">
              <dt className="text-neutral-500">{k}:</dt>
              <dd className="text-neutral-800">{v == null || v === '' ? '—' : String(v)}</dd>
            </div>
          ))}
        </dl>
      )}

      {error && <div className="mt-3 p-2 bg-red-50 border border-red-200 text-red-700 rounded text-sm">{error}</div>}

      <form onSubmit={submit} className="mt-4 flex flex-col sm:flex-row gap-3 sm:items-end">
        <label className="text-sm text-neutral-600">Decision
          <select value={decision} onChange={e => setDecision(e.target.value)} className={`${inputClass} mt-1`}>
            <option value="select">Select</option>
            <option value="reject">Reject</option>
          </select>
        </label>
        <label className="text-sm text-neutral-600 flex-1">Screening notes
          <input value={description} onChange={e => setDescription(e.target.value)} placeholder="Reviewer description" className={`${inputClass} mt-1`} />
        </label>
        <Button variant="accent" type="submit" disabled={saving}>{saving ? 'Saving...' : 'Submit review'}</Button>
      </form>
    </Card>
  )
}

export default function Reviewer(){
  const { user } = useContext(AuthContext)
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
    <div>
      <PageHeader title="Profile Screening" subtitle={`Welcome, ${user?.full_name || ''}.`} />
      <ErrorBanner>{error}</ErrorBanner>
      <section id="reviews" className="scroll-mt-20">
        {items.length === 0 ? (
          <EmptyState>No applications are assigned to you yet.</EmptyState>
        ) : (
          <ul className="space-y-4">
            {items.map(item => <ReviewCard key={item.review_id} item={item} onSubmitted={load} />)}
          </ul>
        )}
      </section>
    </div>
  )
}
