import React, { useEffect, useState } from 'react'
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

  // Cohort-configured extra fields (the in-app dynamic form).
  const [cohortId, setCohortId] = useState(null)
  const [dynFields, setDynFields] = useState([])
  const [dynAnswers, setDynAnswers] = useState({})

  useEffect(() => {
    async function loadForm(){
      try {
        const { data: cohorts } = await api.get('/api/public/cohorts')
        const cohort = cohorts[0]
        if (!cohort) return
        setCohortId(cohort.id)
        const { data: fields } = await api.get(`/api/public/cohorts/${cohort.id}/form`)
        setDynFields(fields)
      } catch {
        /* the base form still works without a configured cohort form */
      }
    }
    loadForm()
  }, [])

  function update(field){
    return (e) => setForm({ ...form, [field]: e.target.value })
  }
  function updateDyn(name){
    return (e) => setDynAnswers({ ...dynAnswers, [name]: e.target.value })
  }

  async function handleSubmit(e){
    e.preventDefault()
    setError('')
    setSubmitting(true)
    try {
      // Single public endpoint runs create-user → profile → application →
      // submit server-side (role pinned to mentee). Server validates required
      // form fields against the cohort's configured form.
      await api.post('/api/public/apply/student', {
        full_name: form.fullName,
        email: form.email,
        country: form.country,
        rural_urban: form.ruralUrban,
        education: form.education,
        score: form.score,
        gender: form.gender,
        about: form.about,
        cohort_id: cohortId,
        answers: dynAnswers,
      })

      setDone(true)
      setForm(EMPTY)
      setDynAnswers({})
    } catch (err) {
      const detail = err?.response?.data?.error?.message || err?.response?.data?.detail
      setError(typeof detail === 'string' ? detail : (err.message || 'Something went wrong. Please try again.'))
    } finally {
      setSubmitting(false)
    }
  }

  function renderDynField(f){
    const val = dynAnswers[f.field_name] ?? ''
    const common = {
      value: val,
      onChange: updateDyn(f.field_name),
      required: f.is_required,
      className: 'mt-1 block w-full border border-gray-300 rounded px-3 py-2',
    }
    if (f.field_type === 'textarea') return <textarea rows="4" {...common} />
    if (f.field_type === 'number') return <input type="number" step="any" {...common} />
    if (f.field_type === 'date') return <input type="date" {...common} />
    if (f.field_type === 'boolean') {
      return (
        <select {...common}>
          <option value="">Select an option</option>
          <option value="true">Yes</option>
          <option value="false">No</option>
        </select>
      )
    }
    if (f.field_type === 'dropdown' || f.field_type === 'multi_select') {
      return (
        <select {...common}>
          <option value="">Select an option</option>
          {(f.options || []).map((o, i) => <option key={i} value={o}>{o}</option>)}
        </select>
      )
    }
    return <input type="text" {...common} />
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

        {/* Cohort-configured additional questions */}
        {dynFields.map((f) => (
          <div key={f.field_name}>
            <label className="block text-sm font-medium text-gray-700">
              {f.field_name}{f.is_required && <span className="text-red-600"> *</span>}
            </label>
            {renderDynField(f)}
          </div>
        ))}

        <div className="flex justify-end">
          <button type="submit" disabled={submitting} className="px-6 py-3 bg-black text-yellow-400 font-semibold rounded hover:bg-gray-900 disabled:opacity-50">
            {submitting ? 'Submitting...' : 'Submit'}
          </button>
        </div>
      </form>
    </div>
  )
}
