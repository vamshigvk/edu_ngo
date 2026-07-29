import React, { useContext, useEffect, useState } from 'react'
import api from '../../services/api'
import { AuthContext } from '../../context/AuthContext'
import DeclarationBanner from '../../components/common/DeclarationBanner'
import WorkshopsSection from '../../components/common/WorkshopsSection'
import EnglishSupportToggle from '../../components/common/EnglishSupportToggle'
import { PageHeader, Stat, Panel, Card, DataTable, Button, ErrorBanner, EmptyState, inputClass } from '../../components/ui'

export default function Mentor(){
  const { user, signDeclaration } = useContext(AuthContext)
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
    <div>
      <PageHeader title="Mentor Dashboard" subtitle={`Welcome, ${user?.full_name || ''}.`} />
      <ErrorBanner>{error}</ErrorBanner>
      <DeclarationBanner user={user} signDeclaration={signDeclaration} role="mentor" />

      {/* Overview */}
      <section id="overview" className="scroll-mt-20">
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
          <Stat label="Assigned mentees" value={metrics.assigned_mentees ?? '—'} />
          <Stat label="Active mentees" value={metrics.active_mentees ?? '—'} />
          <Stat label="Completed check-ins" value={metrics.completed_checkins ?? '—'} />
          <Stat label="Pending check-ins" value={metrics.pending_checkins ?? '—'} />
        </div>

        {profile && (
          <Panel title="Your profile" className="mt-6">
            <div className="text-sm text-neutral-700 space-y-1">
              <p><span className="font-medium">Expertise:</span> {profile.expertise?.length ? profile.expertise.join(', ') : '—'}</p>
              <p><span className="font-medium">Capacity:</span> up to {profile.max_mentees} mentee(s)</p>
              <p><span className="font-medium">Availability:</span> {profile.availability || '—'}</p>
              {profile.bio && <p className="text-neutral-600 whitespace-pre-wrap mt-2">{profile.bio}</p>}
            </div>
          </Panel>
        )}

        {data?.assigned_cohorts?.length > 0 && (
          <Panel title="Your cohorts" className="mt-6">
            <ul className="space-y-2">
              {data.assigned_cohorts.map((c, i) => (
                <li key={i} className="flex justify-between text-sm">
                  <span className="font-medium text-neutral-800">{c.name} <span className="text-xs uppercase text-neutral-400">({c.status})</span></span>
                  <span className="text-neutral-500">{c.start_date || '?'} → {c.end_date || '?'}</span>
                </li>
              ))}
            </ul>
          </Panel>
        )}
      </section>

      {/* Mentees */}
      <section id="mentees" className="scroll-mt-20 mt-10">
        <h2 className="text-lg font-semibold text-neutral-800 mb-3">Your mentees</h2>
        <DataTable
          columns={[
            { key: 'name', label: 'Name' },
            { key: 'email', label: 'Email', render: (m) => m.email || '—' },
            { key: 'cohort_name', label: 'Cohort', render: (m) => m.cohort_name || '—' },
            { key: 'status', label: 'Status', className: 'capitalize' },
            { key: 'match_score', label: 'Match score' },
          ]}
          rows={mentees}
          rowKey={(m, i) => i}
          empty="You have no assigned mentees yet."
        />
      </section>

      {/* Documents */}
      <section id="documents" className="scroll-mt-20 mt-10">
        <h2 className="text-lg font-semibold text-neutral-800 mb-3">Documents to review</h2>
        {docs.length === 0 ? <EmptyState>No documents assigned to you.</EmptyState> : (
          <ul className="space-y-3">
            {docs.map(d => (
              <Card as="li" key={d.id} className="p-4">
                <div className="flex justify-between items-center">
                  <a href={d.url} target="_blank" rel="noreferrer" className="text-yellow-700 font-semibold hover:underline">{d.title}</a>
                  <span className="text-xs text-neutral-500">from {d.applicant_name || 'mentee'} · {String(d.status).replace('_', ' ')}</span>
                </div>
                <div className="mt-2 flex gap-2 items-end">
                  <textarea value={feedback[d.id] ?? d.feedback ?? ''} onChange={e => setFeedback({ ...feedback, [d.id]: e.target.value })}
                    rows="2" placeholder="Your feedback" className={inputClass} />
                  <Button variant="accent" onClick={() => submitReview(d.id)}>Submit</Button>
                </div>
              </Card>
            ))}
          </ul>
        )}
      </section>

      {/* Workshops */}
      <section id="workshops" className="scroll-mt-20 mt-10">
        <WorkshopsSection canSignup />
      </section>

      <Card className="mt-10 p-5">
        <h2 className="text-base font-semibold text-neutral-800 mb-2">Get involved</h2>
        <ul className="list-disc list-inside text-sm text-neutral-700 space-y-1 mb-3">
          <li>Confirm your availability to mentor for the current cycle.</li>
          <li>Sign up to be a panellist in mentee-only and public workshops.</li>
          <li>Review university application documents for your assigned mentees.</li>
        </ul>
        {profile && <EnglishSupportToggle initial={profile.english_support_opt_in} />}
      </Card>
    </div>
  )
}
