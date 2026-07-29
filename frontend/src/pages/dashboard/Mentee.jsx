import React, { useContext, useEffect, useState } from 'react'
import api from '../../services/api'
import { AuthContext } from '../../context/AuthContext'
import DeclarationBanner from '../../components/common/DeclarationBanner'
import WorkshopsSection from '../../components/common/WorkshopsSection'
import EnglishSupportToggle from '../../components/common/EnglishSupportToggle'
import CloseoutSection from '../../components/common/CloseoutSection'
import { PageHeader, Stat, Panel, Card, DataTable, Button, Badge, ErrorBanner, EmptyState, inputClass } from '../../components/ui'

const EMPTY_DOC = { title: '', url: '', doc_type: 'cv' }

export default function Mentee(){
  const { user, signDeclaration } = useContext(AuthContext)
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
    <div>
      <PageHeader title="Mentee Dashboard" subtitle={`Welcome, ${user?.full_name || ''}.`} />
      <ErrorBanner>{error}</ErrorBanner>
      <DeclarationBanner user={user} signDeclaration={signDeclaration} role="mentee" />

      {/* Overview */}
      <section id="overview" className="scroll-mt-20">
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
          <Stat label="Mentor match" value={status.has_active_match ? 'Matched' : 'Pending'} />
          <Stat label="Application" value={status.application_status ? String(status.application_status).replace('_', ' ') : '—'} />
          <Stat label="Completed check-ins" value={status.logged_checkins_count ?? '—'} />
          <Stat label="Upcoming check-ins" value={status.upcoming_checkins_count ?? '—'} />
        </div>

        {profile && (
          <Panel title="Your profile" className="mt-6">
            <div className="grid grid-cols-2 gap-x-8 gap-y-1 text-sm text-neutral-700">
              <p><span className="font-medium">Country:</span> {profile.country || '—'}</p>
              <p><span className="font-medium">Level:</span> {profile.level || '—'}</p>
              <p><span className="font-medium">University:</span> {profile.university || '—'}</p>
              <p><span className="font-medium">Course:</span> {profile.course || '—'}</p>
            </div>
          </Panel>
        )}
      </section>

      {/* Mentor */}
      <section id="mentor" className="scroll-mt-20 mt-10">
        <h2 className="text-lg font-semibold text-neutral-800 mb-3">Your mentor</h2>
        {mentor ? (
          <Card className="p-5">
            <p className="text-lg font-medium text-neutral-900">{mentor.name}</p>
            {mentor.email && <p className="text-neutral-600">{mentor.email}</p>}
            <p className="text-neutral-600 mt-1 text-sm">
              Cohort: {mentor.cohort_name || '—'} · Status: <span className="capitalize">{mentor.status}</span> · Match score: {mentor.match_score}
            </p>
          </Card>
        ) : (
          <EmptyState>You haven't been matched with a mentor yet.</EmptyState>
        )}
      </section>

      {/* Check-ins */}
      <section id="checkins" className="scroll-mt-20 mt-10">
        <h2 className="text-lg font-semibold text-neutral-800 mb-3">Your check-ins</h2>
        <DataTable
          columns={[
            { key: 'sequence_number', label: '#' },
            { key: 'date', label: 'Date', render: (c) => c.date || '—' },
            { key: 'status', label: 'Status', className: 'capitalize' },
            { key: 'notes', label: 'Notes', render: (c) => <span className="text-neutral-500">{c.notes || '—'}</span> },
          ]}
          rows={checkins}
          rowKey={(c, i) => i}
          empty="No check-ins scheduled yet."
        />
      </section>

      {/* Documents */}
      <section id="documents" className="scroll-mt-20 mt-10">
        <h2 className="text-lg font-semibold text-neutral-800 mb-3">Application documents</h2>
        <p className="text-neutral-500 text-sm mb-3">Submit CVs, SoPs, and application drafts (by link) for review.</p>
        <form onSubmit={addDoc} className="grid grid-cols-1 sm:grid-cols-4 gap-3 mb-4">
          <input value={newDoc.title} onChange={e => setNewDoc({...newDoc, title: e.target.value})} placeholder="Title" required className={inputClass} />
          <input value={newDoc.url} onChange={e => setNewDoc({...newDoc, url: e.target.value})} placeholder="Document URL" required className={`${inputClass} sm:col-span-2`} />
          <select value={newDoc.doc_type} onChange={e => setNewDoc({...newDoc, doc_type: e.target.value})} className={inputClass}>
            <option value="cv">CV</option>
            <option value="sop">SoP</option>
            <option value="writing_sample">Writing sample</option>
            <option value="other">Other</option>
          </select>
          <div className="sm:col-span-4">
            <Button variant="accent" type="submit" disabled={savingDoc}>{savingDoc ? 'Uploading...' : 'Submit document'}</Button>
          </div>
        </form>
        {docs.length === 0 ? <EmptyState>No documents submitted yet.</EmptyState> : (
          <ul className="space-y-2">
            {docs.map(d => (
              <Card as="li" key={d.id} className="p-3">
                <div className="flex justify-between items-center">
                  <a href={d.url} target="_blank" rel="noreferrer" className="text-yellow-700 font-semibold hover:underline">{d.title}</a>
                  <Badge>{String(d.status).replace('_', ' ')}</Badge>
                </div>
                {d.feedback && <p className="mt-1 text-sm text-neutral-700"><span className="font-medium">Feedback:</span> {d.feedback}</p>}
              </Card>
            ))}
          </ul>
        )}
      </section>

      {/* Workshops */}
      <section id="workshops" className="scroll-mt-20 mt-10">
        <WorkshopsSection />
      </section>

      {/* Close-out */}
      <section id="closeout" className="scroll-mt-20 mt-10">
        <CloseoutSection />
      </section>

      <Card className="mt-10 p-5">
        <h2 className="text-base font-semibold text-neutral-800 mb-2">Your mentorship journey</h2>
        <ul className="list-disc list-inside text-sm text-neutral-700 space-y-1 mb-3">
          <li>Attend mentee-only and public workshops alongside one-on-one mentorship.</li>
          <li>Submit scholarship applications for review via the Support Programme.</li>
          <li>Join the mentee WhatsApp group to stay in touch with the team.</li>
        </ul>
        {profile && <EnglishSupportToggle initial={profile.english_support_opt_in} />}
      </Card>
    </div>
  )
}
