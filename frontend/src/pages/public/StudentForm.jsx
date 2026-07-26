import React, { useState } from 'react'
import api from '../../services/api'

const EMPTY = {
  fullName: '',
  email: '',
  country: '',
  ruralUrban: '',
  education: '',
  score: '',
  gender: '',
  about: '',
}

export default function StudentForm(){
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
      // A mentee application must be attached to a cohort — use the first
      // active cohort (fall back to any cohort) exposed by the backend.
      const { data: cohorts } = await api.get('/api/cohorts', { params: { limit: 100 } })
      const cohort = cohorts.find(c => c.status === 'active') || cohorts[0]
      if (!cohort) {
        throw new Error('No cohort is currently open for applications.')
      }

      // 1) Create the applicant user (no password — they are not logging in yet).
      const { data: user } = await api.post('/api/users', {
        email: form.email,
        full_name: form.fullName,
        role: 'mentee',
      })

      // 2) Capture their mentee profile.
      await api.post('/api/mentee-profiles', {
        user_id: user.id,
        country: form.country,
        level: form.education,
        cohort_id: cohort.id,
      })

      // 3) Create the application, then submit it.
      const { data: application } = await api.post('/api/applications', {
        user_id: user.id,
        cohort_id: cohort.id,
        purpose: 'skill_building',
        status: 'draft',
        answers: {
          rural_urban: form.ruralUrban,
          highest_education: form.education,
          score: form.score,
          gender: form.gender,
          about: form.about,
        },
      })
      await api.post(`/api/applications/${application.id}/submit`)

      setDone(true)
      setForm(EMPTY)
    } catch (err) {
      const detail = err?.response?.data?.detail
      setError(typeof detail === 'string' ? detail : (err.message || 'Something went wrong. Please try again.'))
    } finally {
      setSubmitting(false)
    }
  }

  if (done) {
    return (
      <div className="max-w-3xl mx-auto px-4 py-12">
        <h1 className="text-3xl font-bold text-black">Application received</h1>
        <p className="mt-4 text-gray-700">Thanks for applying! Our team will review your application and get in touch.</p>
        <button onClick={() => setDone(false)} className="mt-6 px-6 py-3 bg-black text-yellow-400 font-semibold rounded hover:bg-gray-900">
          Submit another application
        </button>
      </div>
    )
  }

  return (
    <div className="max-w-3xl mx-auto px-4 py-12">
      <h1 className="text-3xl font-bold text-black">Student Application</h1>

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
          <label className="block text-sm font-medium text-gray-700">Rural/Urban</label>
          <select value={form.ruralUrban} onChange={update('ruralUrban')} required className="mt-1 block w-full border border-gray-300 rounded px-3 py-2">
            <option value="">Select an option</option>
            <option value="rural">Rural</option>
            <option value="urban">Urban</option>
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700">Highest Education</label>
          <select value={form.education} onChange={update('education')} required className="mt-1 block w-full border border-gray-300 rounded px-3 py-2">
            <option value="">Select an option</option>
            <option value="high-school">High School</option>
            <option value="diploma">Diploma</option>
            <option value="bachelors">Bachelors</option>
            <option value="masters">Masters</option>
            <option value="phd">PhD</option>
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700">Score in that Education</label>
          <input type="number" step="0.01" value={form.score} onChange={update('score')} required className="mt-1 block w-full border border-gray-300 rounded px-3 py-2" />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700">Gender</label>
          <select value={form.gender} onChange={update('gender')} required className="mt-1 block w-full border border-gray-300 rounded px-3 py-2">
            <option value="">Select an option</option>
            <option value="male">Male</option>
            <option value="female">Female</option>
            <option value="other">Other</option>
          </select>
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
