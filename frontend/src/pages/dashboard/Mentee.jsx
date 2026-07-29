import React, { useContext, useEffect, useState } from 'react'
import api from '../../services/api'
import { AuthContext } from '../../context/AuthContext'
import DeclarationBanner from '../../components/common/DeclarationBanner'
import WorkshopsSection from '../../components/common/WorkshopsSection'
import EnglishSupportToggle from '../../components/common/EnglishSupportToggle'
import CloseoutSection from '../../components/common/CloseoutSection'

function Stat({ label, value }){
  return (
    <div className="p-5 rounded-lg bg-yellow-100">
      <p className="text-sm text-gray-600">{label}</p>
      <p className="text-2xl font-bold text-gray-900">{value}</p>
    </div>
  )
}

const EMPTY_DOC = { title: '', url: '', doc_type: 'cv' }

export default function Mentee(){
  const { user, logout, signDeclaration } = useContext(AuthContext)
  const [data, setData] = useState(null)
  const [error, setError] = useState('')
  const [docs, setDocs] = useState([])
  const [newDoc, setNewDoc] = useState(EMPTY_DOC)
  const [savingDoc, setSavingDoc] = useState(false)

  async function loadDocs(){
    try { setDocs((await api.get('/api/documents/mine')).data) } catch { /* ignore */ }
  }
  async function addDoc(e){
    e.preventDefault()
    if (!newDoc.title || !newDoc.url) return
    setSavingDoc(true)
    try { await api.post('/api/documents', newDoc); setNewDoc(EMPTY_DOC); await loadDocs() }
    catch (err) { setError(err?.response?.data?.error?.message || 'Could not upload the document.') }
    finally { setSavingDoc(false) }
  }

  useEffect(() => {
    async function load(){
      try {
        const { data } = await api.get('/dashboard/mentee')
        setData(data)
      } catch (err) {
        const detail = err?.response?.data?.error?.message
        setError(typeof detail === 'string' ? detail : 'Could not load your dashboard.')
      }
      await loadDocs()
    }
    load()
  }, [])

  const status = data?.my_program_status || {}
  const mentor = data?.mentor
  const profile = data?.profile
  const checkins = data?.checkins || []

  return (
    <div className="max-w-5xl mx-auto px-4 py-10">
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Mentee Dashboard</h1>
          <p className="text-gray-600 mt-1">Welcome, {user?.full_name}.</p>
        </div>
        <button onClick={logout} className="px-4 py-2 bg-black text-yellow-400 font-semibold rounded hover:bg-gray-900">
          Logout
        </button>
      </div>

      {error && <div className="mb-6 p-3 bg-red-100 border border-red-400 text-red-700 rounded">{error}</div>}

      <DeclarationBanner user={user} signDeclaration={signDeclaration} role="mentee" />

      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 mb-10">
        <Stat label="Mentor match" value={status.has_active_match ? 'Matched' : 'Pending'} />
        <Stat label="Application" value={status.application_status ? String(status.application_status).replace('_', ' ') : '—'} />
        <Stat label="Completed check-ins" value={status.logged_checkins_count ?? '—'} />
        <Stat label="Upcoming check-ins" value={status.upcoming_checkins_count ?? '—'} />
      </div>

      <section className="mb-10">
        <h2 className="text-xl font-semibold text-gray-800 mb-3">Your mentor</h2>
        {mentor ? (
          <div className="p-5 rounded-lg bg-white border">
            <p className="text-lg font-medium text-gray-900">{mentor.name}</p>
            {mentor.email && <p className="text-gray-600">{mentor.email}</p>}
            <p className="text-gray-600 mt-1">
              Cohort: {mentor.cohort_name || '—'} · Status:{' '}
              <span className="capitalize">{mentor.status}</span> · Match score: {mentor.match_score}
            </p>
          </div>
        ) : (
          <p className="text-gray-600">You haven't been matched with a mentor yet.</p>
        )}
      </section>

      <section className="mb-10">
        <h2 className="text-xl font-semibold text-gray-800 mb-3">Your check-ins</h2>
        {checkins.length ? (
          <div className="overflow-x-auto rounded-lg border border-gray-200">
            <table className="min-w-full table-auto border-collapse">
              <thead className="bg-gray-50">
                <tr className="text-left">
                  <th className="py-2 px-3">#</th>
                  <th className="py-2 px-3">Date</th>
                  <th className="py-2 px-3">Status</th>
                  <th className="py-2 px-3">Notes</th>
                </tr>
              </thead>
              <tbody>
                {checkins.map((c, i) => (
                  <tr key={i} className="border-t hover:bg-yellow-50">
                    <td className="py-2 px-3">{c.sequence_number}</td>
                    <td className="py-2 px-3">{c.date || '—'}</td>
                    <td className="py-2 px-3 capitalize">{c.status}</td>
                    <td className="py-2 px-3 text-sm text-gray-600">{c.notes || '—'}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <p className="text-gray-600">No check-ins scheduled yet.</p>
        )}
      </section>

      {profile && (
        <section className="mb-10 p-5 rounded-lg bg-white border">
          <h2 className="text-lg font-semibold text-gray-800 mb-2">Your profile</h2>
          <p className="text-gray-700"><span className="font-medium">Country:</span> {profile.country || '—'}</p>
          <p className="text-gray-700"><span className="font-medium">Level:</span> {profile.level || '—'}</p>
          <p className="text-gray-700"><span className="font-medium">University:</span> {profile.university || '—'}</p>
          <p className="text-gray-700"><span className="font-medium">Course:</span> {profile.course || '—'}</p>
        </section>
      )}

      <section className="mb-10">
        <h2 className="text-xl font-semibold text-gray-800 mb-3">Application documents</h2>
        <p className="text-gray-600 text-sm mb-3">Submit CVs, SoPs, and application drafts (by link) for review.</p>
        <form onSubmit={addDoc} className="grid grid-cols-1 sm:grid-cols-4 gap-3 mb-4">
          <input value={newDoc.title} onChange={e => setNewDoc({...newDoc, title: e.target.value})} placeholder="Title" required className="p-2 rounded border" />
          <input value={newDoc.url} onChange={e => setNewDoc({...newDoc, url: e.target.value})} placeholder="Document URL" required className="p-2 rounded border sm:col-span-2" />
          <select value={newDoc.doc_type} onChange={e => setNewDoc({...newDoc, doc_type: e.target.value})} className="p-2 rounded border">
            <option value="cv">CV</option>
            <option value="sop">SoP</option>
            <option value="writing_sample">Writing sample</option>
            <option value="other">Other</option>
          </select>
          <div className="sm:col-span-4">
            <button disabled={savingDoc} className="px-4 py-2 bg-yellow-600 text-white rounded disabled:opacity-50">
              {savingDoc ? 'Uploading...' : 'Submit document'}
            </button>
          </div>
        </form>
        {docs.length === 0 ? <p className="text-gray-600">No documents submitted yet.</p> : (
          <ul className="space-y-2">
            {docs.map(d => (
              <li key={d.id} className="p-3 bg-white rounded shadow-sm border">
                <div className="flex justify-between items-center">
                  <a href={d.url} target="_blank" rel="noreferrer" className="text-yellow-600 font-semibold">{d.title}</a>
                  <span className="text-xs uppercase px-2 py-0.5 rounded bg-gray-100 text-gray-600">{String(d.status).replace('_', ' ')}</span>
                </div>
                {d.feedback && <p className="mt-1 text-sm text-gray-700"><span className="font-medium">Feedback:</span> {d.feedback}</p>}
              </li>
            ))}
          </ul>
        )}
      </section>

      <WorkshopsSection />

      <CloseoutSection />

      <section className="p-5 rounded-lg bg-gray-50 border">
        <h2 className="text-lg font-semibold text-gray-800 mb-2">Your mentorship journey</h2>
        <ul className="list-disc list-inside text-gray-700 space-y-1 mb-3">
          <li>Attend mentee-only and public workshops alongside one-on-one mentorship.</li>
          <li>Submit scholarship applications for review via the Support Programme.</li>
          <li>Join the mentee WhatsApp group to stay in touch with the team.</li>
        </ul>
        {profile && <EnglishSupportToggle initial={profile.english_support_opt_in} />}
      </section>
    </div>
  )
}
