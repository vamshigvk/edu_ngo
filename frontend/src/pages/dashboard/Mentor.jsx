import React, { useContext, useEffect, useState } from 'react'
import api from '../../services/api'
import { AuthContext } from '../../context/AuthContext'
import DeclarationBanner from '../../components/common/DeclarationBanner'
import WorkshopsSection from '../../components/common/WorkshopsSection'
import EnglishSupportToggle from '../../components/common/EnglishSupportToggle'

function Stat({ label, value }){
  return (
    <div className="p-5 rounded-lg bg-yellow-100">
      <p className="text-sm text-gray-600">{label}</p>
      <p className="text-3xl font-bold text-gray-900">{value}</p>
    </div>
  )
}

export default function Mentor(){
  const { user, logout, signDeclaration } = useContext(AuthContext)
  const [data, setData] = useState(null)
  const [error, setError] = useState('')
  const [docs, setDocs] = useState([])
  const [feedback, setFeedback] = useState({}) // docId -> feedback text

  async function loadDocs(){
    try { setDocs((await api.get('/api/documents/assigned')).data) } catch { /* ignore */ }
  }
  async function submitReview(docId){
    try { await api.post(`/api/documents/${docId}/review`, { feedback: feedback[docId] || '' }); await loadDocs() }
    catch (err) { setError(err?.response?.data?.error?.message || 'Could not submit feedback.') }
  }

  useEffect(() => {
    async function load(){
      try {
        const { data } = await api.get('/dashboard/mentor')
        setData(data)
      } catch (err) {
        const detail = err?.response?.data?.error?.message
        setError(typeof detail === 'string' ? detail : 'Could not load your dashboard.')
      }
      await loadDocs()
    }
    load()
  }, [])

  const metrics = data?.engagement_metrics || {}
  const profile = data?.profile
  const mentees = data?.mentees || []

  return (
    <div className="max-w-5xl mx-auto px-4 py-10">
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Mentor Dashboard</h1>
          <p className="text-gray-600 mt-1">Welcome, {user?.full_name}.</p>
        </div>
        <button onClick={logout} className="px-4 py-2 bg-black text-yellow-400 font-semibold rounded hover:bg-gray-900">
          Logout
        </button>
      </div>

      {error && <div className="mb-6 p-3 bg-red-100 border border-red-400 text-red-700 rounded">{error}</div>}

      <DeclarationBanner user={user} signDeclaration={signDeclaration} role="mentor" />

      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 mb-10">
        <Stat label="Assigned mentees" value={metrics.assigned_mentees ?? '—'} />
        <Stat label="Active mentees" value={metrics.active_mentees ?? '—'} />
        <Stat label="Completed check-ins" value={metrics.completed_checkins ?? '—'} />
        <Stat label="Pending check-ins" value={metrics.pending_checkins ?? '—'} />
      </div>

      {profile && (
        <section className="mb-10 p-5 rounded-lg bg-white border">
          <h2 className="text-lg font-semibold text-gray-800 mb-2">Your profile</h2>
          <p className="text-gray-700"><span className="font-medium">Expertise:</span> {profile.expertise?.length ? profile.expertise.join(', ') : '—'}</p>
          <p className="text-gray-700"><span className="font-medium">Capacity:</span> up to {profile.max_mentees} mentee(s)</p>
          <p className="text-gray-700"><span className="font-medium">Availability:</span> {profile.availability || '—'}</p>
          {profile.bio && <p className="text-gray-600 mt-2 whitespace-pre-wrap">{profile.bio}</p>}
        </section>
      )}

      <section className="mb-10">
        <h2 className="text-xl font-semibold text-gray-800 mb-3">Your mentees</h2>
        {mentees.length ? (
          <div className="overflow-x-auto rounded-lg border border-gray-200">
            <table className="min-w-full table-auto border-collapse">
              <thead className="bg-gray-50">
                <tr className="text-left">
                  <th className="py-2 px-3">Name</th>
                  <th className="py-2 px-3">Email</th>
                  <th className="py-2 px-3">Cohort</th>
                  <th className="py-2 px-3">Status</th>
                  <th className="py-2 px-3">Match Score</th>
                </tr>
              </thead>
              <tbody>
                {mentees.map((m, i) => (
                  <tr key={i} className="border-t hover:bg-yellow-50">
                    <td className="py-2 px-3">{m.name}</td>
                    <td className="py-2 px-3">{m.email || '—'}</td>
                    <td className="py-2 px-3">{m.cohort_name || '—'}</td>
                    <td className="py-2 px-3 capitalize">{m.status}</td>
                    <td className="py-2 px-3">{m.match_score}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <p className="text-gray-600">You have no assigned mentees yet.</p>
        )}
      </section>

      <section className="mb-10">
        <h2 className="text-xl font-semibold text-gray-800 mb-3">Your cohorts</h2>
        {data?.assigned_cohorts?.length ? (
          <ul className="space-y-2">
            {data.assigned_cohorts.map((c, i) => (
              <li key={i} className="p-4 bg-white rounded shadow-sm flex justify-between border">
                <span className="font-medium text-gray-800">{c.name} <span className="text-xs uppercase text-gray-400">({c.status})</span></span>
                <span className="text-gray-500 text-sm">{c.start_date || '?'} → {c.end_date || '?'}</span>
              </li>
            ))}
          </ul>
        ) : (
          <p className="text-gray-600">You are not yet assigned to a cohort.</p>
        )}
      </section>

      <section className="mb-10">
        <h2 className="text-xl font-semibold text-gray-800 mb-3">Documents to review</h2>
        {docs.length === 0 ? <p className="text-gray-600">No documents assigned to you.</p> : (
          <ul className="space-y-3">
            {docs.map(d => (
              <li key={d.id} className="p-4 bg-white rounded shadow-sm border">
                <div className="flex justify-between items-center">
                  <a href={d.url} target="_blank" rel="noreferrer" className="text-yellow-600 font-semibold">{d.title}</a>
                  <span className="text-xs text-gray-500">from {d.applicant_name || 'mentee'} · {String(d.status).replace('_', ' ')}</span>
                </div>
                <div className="mt-2 flex gap-2 items-end">
                  <textarea value={feedback[d.id] ?? d.feedback ?? ''} onChange={e => setFeedback({ ...feedback, [d.id]: e.target.value })}
                    rows="2" placeholder="Your feedback" className="flex-1 p-2 rounded border text-sm" />
                  <button onClick={() => submitReview(d.id)} className="px-3 py-2 bg-yellow-600 text-white rounded text-sm">Submit</button>
                </div>
              </li>
            ))}
          </ul>
        )}
      </section>

      <WorkshopsSection canSignup />

      <section className="p-5 rounded-lg bg-gray-50 border">
        <h2 className="text-lg font-semibold text-gray-800 mb-2">Get involved</h2>
        <ul className="list-disc list-inside text-gray-700 space-y-1 mb-3">
          <li>Confirm your availability to mentor for the current cycle.</li>
          <li>Sign up to be a panellist in mentee-only and public workshops.</li>
          <li>Review university application documents for your assigned mentees.</li>
        </ul>
        {profile && <EnglishSupportToggle initial={profile.english_support_opt_in} />}
      </section>
    </div>
  )
}
