import React, { useState } from 'react'
import api from '../../services/api'

const EMPTY = { fullName: '', email: '', country: '', discipline: '', about: '', studiedAbroad: false }

export default function MentorForm(){
  const [form, setForm] = useState(EMPTY)
  const [submitting, setSubmitting] = useState(false)
  const [error, setError] = useState('')
  const [done, setDone] = useState(false)

  function update(field){
    return (e) => setForm({ ...form, [field]: e.target.value })
  }

  async function handleSubmit(e){
    e.preventDefault()
    setError('')
    setSubmitting(true)
    try {
      // Public endpoint creates the mentor user + profile (role pinned to mentor).
      await api.post('/api/public/apply/mentor', {
        full_name: form.fullName,
        email: form.email,
        country: form.country,
        discipline: form.discipline,
        about: form.about,
        studied_abroad: form.studiedAbroad,
      })

      setDone(true)
      setForm(EMPTY)
    } catch (err) {
      const detail = err?.response?.data?.error?.message || err?.response?.data?.detail
      setError(typeof detail === 'string' ? detail : (err.message || 'Something went wrong. Please try again.'))
    } finally {
      setSubmitting(false)
    }
  }

  if (done) {
    return (
      <div className="max-w-3xl mx-auto px-4 py-12">
        <h1 className="text-3xl font-bold text-black">Thanks for volunteering!</h1>
        <p className="mt-4 text-gray-700">Your mentor profile has been created. We'll reach out with next steps.</p>
        <button onClick={() => setDone(false)} className="mt-6 px-6 py-3 bg-black text-yellow-400 font-semibold rounded hover:bg-gray-900">
          Register another mentor
        </button>
      </div>
    )
  }

  return (
    <div className="max-w-3xl mx-auto px-4 py-12">
      <h1 className="text-3xl font-bold text-black">Mentor Application</h1>

      {error && (
        <div className="mt-4 p-3 bg-red-100 border border-red-400 text-red-700 rounded">{error}</div>
      )}

      <form onSubmit={handleSubmit} className="mt-6 bg-white p-6 rounded shadow space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-700">Full name</label>
          <input value={form.fullName} onChange={update('fullName')} required className="mt-1 block w-full border border-gray-300 rounded px-3 py-2" />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700">Email</label>
          <input type="email" value={form.email} onChange={update('email')} required className="mt-1 block w-full border border-gray-300 rounded px-3 py-2" />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700">Country</label>
          <input value={form.country} onChange={update('country')} className="mt-1 block w-full border border-gray-300 rounded px-3 py-2" />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700">Discipline / field of expertise</label>
          <input value={form.discipline} onChange={update('discipline')} placeholder="e.g. Computer Science, Public Health" className="mt-1 block w-full border border-gray-300 rounded px-3 py-2" />
        </div>

        <div>
          <label className="flex items-center gap-2 text-sm font-medium text-gray-700">
            <input type="checkbox" checked={form.studiedAbroad} onChange={(e) => setForm({ ...form, studiedAbroad: e.target.checked })} />
            I have studied abroad
          </label>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700">Tell us about yourself</label>
          <textarea value={form.about} onChange={update('about')} rows="4" className="mt-1 block w-full border border-gray-300 rounded px-3 py-2" />
        </div>

        <div className="flex justify-end">
          <button type="submit" disabled={submitting} className="px-6 py-3 bg-black text-yellow-400 font-semibold rounded hover:bg-gray-900 disabled:opacity-50">
            {submitting ? 'Submitting...' : 'Submit'}
          </button>
        </div>
      </form>
    </div>
  )
}
