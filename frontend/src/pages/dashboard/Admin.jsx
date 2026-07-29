import React, { useContext, useEffect, useState } from 'react'
import api from '../../services/api'
import { AuthContext } from '../../context/AuthContext'

const RESOURCE_TYPES = [
  { value: 'scholarship', label: 'Scholarship' },
  { value: 'course', label: 'Course' },
  { value: 'university_info', label: 'University Info' },
  { value: 'guide', label: 'Guide' },
  { value: 'video', label: 'Video' },
]
const COHORT_STATUSES = ['upcoming', 'active', 'completed', 'archived']
const FIELD_TYPES = ['text', 'textarea', 'number', 'dropdown', 'multi_select', 'date', 'boolean']
const DECISIONS = ['select', 'waitlist', 'reject']

const EMPTY_RESOURCE = { title: '', url: '', type: 'guide', description: '' }
const EMPTY_COHORT = {
  name: '', program: '', start_date: '', end_date: '',
  status: 'active', max_mentees: 20, selection_threshold: 0,
}
const EMPTY_FIELD = { field_name: '', field_type: 'text', is_required: false, field_order: 0, options: '' }
const EMPTY_WORKSHOP = { title: '', description: '', scheduled_date: '', recording_url: '', audience: 'public' }
const PAGE_SIZE = 10

function errText(err, fallback){
  const detail = err?.response?.data?.error?.message || err?.response?.data?.detail
  return typeof detail === 'string' ? detail : fallback
}

export default function Admin(){
  const { user, logout } = useContext(AuthContext)
  const [tab, setTab] = useState('mentors')
  const [error, setError] = useState('')
  const [summary, setSummary] = useState(null)

  // People (mentors / students) — server-side search + pagination.
  const [people, setPeople] = useState([])
  const [peopleTotal, setPeopleTotal] = useState(0)
  const [page, setPage] = useState(0)
  const [searchInput, setSearchInput] = useState('')
  const [search, setSearch] = useState('')

  const [pairs, setPairs] = useState([])

  const [cohorts, setCohorts] = useState([])
  const [newCohort, setNewCohort] = useState(EMPTY_COHORT)
  const [savingCohort, setSavingCohort] = useState(false)

  const [resources, setResources] = useState([])
  const [newResource, setNewResource] = useState(EMPTY_RESOURCE)
  const [savingResource, setSavingResource] = useState(false)

  // Selection pipeline.
  const [board, setBoard] = useState([])
  const [boardCohort, setBoardCohort] = useState('')
  const [reviewers, setReviewers] = useState([])
  const [notifications, setNotifications] = useState([])

  // Mapping.
  const [mapping, setMapping] = useState({ mentees: [], mentors: [] })
  const [mappingCohort, setMappingCohort] = useState('')

  // Documents.
  const [documents, setDocuments] = useState([])
  const [docMentors, setDocMentors] = useState([])

  // Workshops.
  const [workshops, setWorkshops] = useState([])
  const [newWorkshop, setNewWorkshop] = useState(EMPTY_WORKSHOP)
  const [savingWorkshop, setSavingWorkshop] = useState(false)

  // Close of programme.
  const [feedback, setFeedback] = useState([])
  const [offers, setOffers] = useState([])

  const roleFor = (t) => (t === 'mentors' ? 'mentor' : t === 'students' ? 'mentee' : null)

  async function loadPeople(role, pageArg, searchArg){
    if (!role) return
    try {
      const { data } = await api.get('/api/users', {
        params: { role, search: searchArg || undefined, skip: pageArg * PAGE_SIZE, limit: PAGE_SIZE },
      })
      setPeople(data.items); setPeopleTotal(data.total)
    } catch (err) { setError(errText(err, 'Failed to load users.')) }
  }
  async function loadPairs(){
    try { setPairs((await api.get('/api/pairs', { params: { limit: 1000 } })).data) }
    catch (err) { setError(errText(err, 'Failed to load matches.')) }
  }
  async function loadCohorts(){
    try { setCohorts((await api.get('/api/cohorts', { params: { limit: 1000 } })).data) }
    catch (err) { setError(errText(err, 'Failed to load cohorts.')) }
  }
  async function loadResources(){
    try { setResources((await api.get('/api/resources', { params: { limit: 1000 } })).data) }
    catch (err) { setError(errText(err, 'Failed to load resources.')) }
  }
  async function loadBoard(cohortId){
    try {
      const params = cohortId ? { cohort_id: cohortId } : {}
      setBoard((await api.get('/api/applications/review-board', { params })).data)
    } catch (err) { setError(errText(err, 'Failed to load applications.')) }
  }
  async function loadReviewers(){
    try {
      const { data } = await api.get('/api/users', { params: { role: 'reviewer', limit: 1000 } })
      setReviewers(data.items)
    } catch (err) { setError(errText(err, 'Failed to load reviewers.')) }
  }
  async function loadNotifications(){
    try { setNotifications((await api.get('/api/notifications', { params: { limit: 200 } })).data) }
    catch (err) { setError(errText(err, 'Failed to load notifications.')) }
  }
  async function loadMapping(cohortId){
    try {
      const params = cohortId ? { cohort_id: cohortId } : {}
      setMapping((await api.get('/api/mapping/board', { params })).data)
    } catch (err) { setError(errText(err, 'Failed to load mapping board.')) }
  }
  async function loadDocuments(){
    try {
      setDocuments((await api.get('/api/documents')).data)
      setDocMentors((await api.get('/api/users', { params: { role: 'mentor', limit: 1000 } })).data.items)
    } catch (err) { setError(errText(err, 'Failed to load documents.')) }
  }
  async function assignDoc(docId, mentorId){
    if (!mentorId) return
    try { await api.post(`/api/documents/${docId}/assign`, { reviewer_id: mentorId }); await loadDocuments() }
    catch (err) { setError(errText(err, 'Failed to assign reviewer.')) }
  }
  async function loadWorkshops(){
    try { setWorkshops((await api.get('/api/workshops')).data) }
    catch (err) { setError(errText(err, 'Failed to load workshops.')) }
  }
  async function addWorkshop(e){
    e.preventDefault()
    if (!newWorkshop.title) return
    setSavingWorkshop(true); setError('')
    try {
      await api.post('/api/workshops', { ...newWorkshop, scheduled_date: newWorkshop.scheduled_date || null })
      setNewWorkshop(EMPTY_WORKSHOP); await loadWorkshops()
    } catch (err) { setError(errText(err, 'Failed to create workshop.')) }
    finally { setSavingWorkshop(false) }
  }
  async function deleteWorkshop(id){
    try { await api.delete(`/api/workshops/${id}`); await loadWorkshops() }
    catch (err) { setError(errText(err, 'Failed to delete workshop.')) }
  }
  async function loadCloseout(){
    try {
      setFeedback((await api.get('/api/closeout/feedback')).data)
      setOffers((await api.get('/api/closeout/offers')).data)
    } catch (err) { setError(errText(err, 'Failed to load close-out data.')) }
  }

  useEffect(() => {
    async function init(){
      try {
        const dash = await api.get('/dashboard/emp')
        setSummary(dash.data.platform_summary)
      } catch (err) { setError(errText(err, 'Failed to load dashboard data.')) }
      await Promise.all([loadPeople('mentor', 0, ''), loadPairs(), loadCohorts(), loadResources()])
    }
    init()
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  function selectTab(t){
    setTab(t); setError('')
    if (roleFor(t)) { setPage(0); setSearch(''); setSearchInput(''); loadPeople(roleFor(t), 0, '') }
    if (t === 'applications') { loadBoard(boardCohort); loadReviewers() }
    if (t === 'mapping') loadMapping(mappingCohort)
    if (t === 'documents') loadDocuments()
    if (t === 'workshops') loadWorkshops()
    if (t === 'closeout') loadCloseout()
    if (t === 'notifications') loadNotifications()
  }

  async function setMenteeType(menteeId, type){
    try { await api.post('/api/mapping/mentee-type', { mentee_id: menteeId, mentorship_type: type }); await loadMapping(mappingCohort) }
    catch (err) { setError(errText(err, 'Failed to set mentorship type.')) }
  }
  async function assignMentor(menteeId, mentorId, cohortId){
    if (!mentorId || !cohortId) { setError('Pick a mentor; the mentee must belong to a cohort.'); return }
    try { await api.post('/api/mapping/pair', { mentor_id: mentorId, mentee_id: menteeId, cohort_id: cohortId }); await loadMapping(mappingCohort) }
    catch (err) { setError(errText(err, 'Failed to create pairing.')) }
  }
  function submitSearch(e){
    e.preventDefault(); setSearch(searchInput); setPage(0)
    loadPeople(roleFor(tab), 0, searchInput)
  }
  function gotoPage(p){ setPage(p); loadPeople(roleFor(tab), p, search) }

  async function addCohort(e){
    e.preventDefault(); setSavingCohort(true); setError('')
    try {
      await api.post('/api/cohorts', {
        ...newCohort,
        max_mentees: Number(newCohort.max_mentees),
        selection_threshold: Number(newCohort.selection_threshold),
      })
      setNewCohort(EMPTY_COHORT); await loadCohorts()
    } catch (err) { setError(errText(err, 'Failed to create cohort.')) }
    finally { setSavingCohort(false) }
  }

  async function addResource(e){
    e.preventDefault()
    if(!newResource.title || !newResource.url) return
    setSavingResource(true); setError('')
    try { await api.post('/api/resources', newResource); setNewResource(EMPTY_RESOURCE); await loadResources() }
    catch (err) { setError(errText(err, 'Failed to add resource.')) }
    finally { setSavingResource(false) }
  }
  async function deleteResource(id){
    try { await api.delete(`/api/resources/${id}`); await loadResources() }
    catch (err) { setError(errText(err, 'Failed to delete resource.')) }
  }

  // --- selection-pipeline actions ---
  async function runScoring(){
    if (!boardCohort) { setError('Select a cohort to run disadvantage scoring.'); return }
    try { await api.post(`/api/cohorts/${boardCohort}/scoring/run`); await loadBoard(boardCohort) }
    catch (err) { setError(errText(err, 'Scoring failed.')) }
  }
  async function assignReviewers(appId, reviewerIds){
    if (!reviewerIds.length) return
    try { await api.post(`/api/applications/${appId}/reviewers`, { reviewer_ids: reviewerIds }); await loadBoard(boardCohort) }
    catch (err) { setError(errText(err, 'Failed to assign reviewers.')) }
  }
  async function computeSystem(appId){
    try { await api.post(`/api/applications/${appId}/system-decision`); await loadBoard(boardCohort) }
    catch (err) { setError(errText(err, 'Failed to compute system decision.')) }
  }
  async function adminDecision(appId, decision, notes){
    try { await api.post(`/api/applications/${appId}/admin-decision`, { decision, notes }); await loadBoard(boardCohort) }
    catch (err) { setError(errText(err, 'Failed to record decision.')) }
  }

  const heading = {
    mentors: 'Mentors', students: 'Students', applications: 'Applications Review',
    mapping: 'Mentee - Mentor Mapping', matches: 'Mentor - Mentee Matches',
    documents: 'Document Review Portal', workshops: 'Workshops',
    closeout: 'Close of Programme', cohorts: 'Cohorts',
    resources: 'Resources', notifications: 'Notifications',
  }[tab]
  const totalPages = Math.max(1, Math.ceil(peopleTotal / PAGE_SIZE))
  const TABS = [
    ['mentors', 'Mentors'], ['students', 'Students'], ['applications', 'Applications'],
    ['mapping', 'Mapping'], ['matches', 'Matches'], ['documents', 'Documents'],
    ['workshops', 'Workshops'], ['closeout', 'Close-out'], ['cohorts', 'Cohorts'],
    ['resources', 'Resources'], ['notifications', 'Notifications'],
  ]

  return (
    <div className="min-h-screen bg-yellow-50">
      <div className="min-h-screen flex flex-col md:flex-row">
        <aside className="md:w-64 w-full bg-gray-900 text-yellow-300 p-6 md:min-h-screen">
          <div className="flex items-center justify-between md:block mb-6">
            <div>
              <h2 className="text-2xl font-semibold">Admin</h2>
              {user && <p className="text-xs text-yellow-500 mt-1">{user.full_name}</p>}
            </div>
            <button onClick={logout} className="px-3 py-2 bg-red-600 rounded text-white md:hidden">Logout</button>
          </div>
          <nav className="space-y-2">
            {TABS.map(([key, label]) => (
              <button key={key} onClick={() => selectTab(key)}
                className={`w-full text-left px-3 py-2 rounded ${tab===key ? 'bg-yellow-700 text-white' : 'hover:bg-yellow-900'}`}>
                {label}
              </button>
            ))}
          </nav>
          <div className="hidden md:block mt-8">
            <button onClick={logout} className="w-full px-3 py-3 bg-red-600 rounded text-white">Logout</button>
          </div>
        </aside>

        <main className="flex-1 p-6 md:p-8 min-h-screen bg-white">
          <div className="max-w-full mx-auto">
            <h3 className="text-3xl font-semibold mb-6 text-gray-800">{heading}</h3>

            {summary && (
              <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-8">
                <div className="p-4 rounded-lg bg-yellow-100"><p className="text-sm text-gray-600">Total Users</p><p className="text-2xl font-bold text-gray-900">{summary.total_users}</p></div>
                <div className="p-4 rounded-lg bg-yellow-100"><p className="text-sm text-gray-600">Active Cohorts</p><p className="text-2xl font-bold text-gray-900">{summary.total_active_cohorts}</p></div>
                <div className="p-4 rounded-lg bg-yellow-100"><p className="text-sm text-gray-600">Applications Under Review</p><p className="text-2xl font-bold text-gray-900">{summary.total_applications_under_review}</p></div>
              </div>
            )}

            {error && <div className="mb-6 p-3 bg-red-100 border border-red-400 text-red-700 rounded">{error}</div>}

            {(tab === 'mentors' || tab === 'students') && (
              <PeopleTable kind={tab} people={people} total={peopleTotal} page={page}
                totalPages={totalPages} searchInput={searchInput} setSearchInput={setSearchInput}
                onSearch={submitSearch} onPage={gotoPage} />
            )}

            {tab === 'applications' && (
              <ApplicationsPanel
                board={board} cohorts={cohorts} reviewers={reviewers}
                boardCohort={boardCohort}
                onCohortChange={(id) => { setBoardCohort(id); loadBoard(id) }}
                onRunScoring={runScoring}
                onAssign={assignReviewers}
                onComputeSystem={computeSystem}
                onDecision={adminDecision}
              />
            )}

            {tab === 'mapping' && (
              <MappingPanel
                mapping={mapping} cohorts={cohorts} mappingCohort={mappingCohort}
                onCohortChange={(id) => { setMappingCohort(id); loadMapping(id) }}
                onSetType={setMenteeType} onAssign={assignMentor}
              />
            )}

            {tab === 'matches' && (
              <div className="overflow-x-auto rounded-lg border border-gray-200">
                <table className="min-w-full table-auto border-collapse">
                  <thead className="bg-gray-50"><tr className="text-left">
                    <th className="py-3 px-4">Mentor</th><th className="py-3 px-4">Student</th>
                    <th className="py-3 px-4">Status</th><th className="py-3 px-4">Match Score</th>
                  </tr></thead>
                  <tbody>
                    {pairs.map(p => (
                      <tr key={p.id} className="border-t hover:bg-yellow-50">
                        <td className="py-3 px-4">{p.mentor_name || p.mentor_id}</td>
                        <td className="py-3 px-4">{p.mentee_name || p.mentee_id}</td>
                        <td className="py-3 px-4 capitalize">{p.status}</td>
                        <td className="py-3 px-4">{p.match_score}</td>
                      </tr>
                    ))}
                    {pairs.length === 0 && <tr><td colSpan="4" className="py-3 px-4 text-gray-500">No matches yet.</td></tr>}
                  </tbody>
                </table>
              </div>
            )}

            {tab === 'documents' && (
              <DocumentsPanel documents={documents} mentors={docMentors} onAssign={assignDoc} />
            )}

            {tab === 'workshops' && (
              <WorkshopsPanel
                workshops={workshops} newWorkshop={newWorkshop} setNewWorkshop={setNewWorkshop}
                saving={savingWorkshop} onCreate={addWorkshop} onDelete={deleteWorkshop}
              />
            )}

            {tab === 'closeout' && (
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                <div>
                  <h4 className="text-lg font-semibold mb-3">Programme feedback</h4>
                  {feedback.length === 0 ? <p className="text-gray-600">No feedback yet.</p> : (
                    <ul className="space-y-2">
                      {feedback.map(f => (
                        <li key={f.id} className="p-3 bg-white rounded border">
                          <p className="font-medium text-gray-800">{f.user_name || 'Mentee'} — {f.rating}/5</p>
                          {f.comments && <p className="text-sm text-gray-600 mt-1">{f.comments}</p>}
                        </li>
                      ))}
                    </ul>
                  )}
                </div>
                <div>
                  <h4 className="text-lg font-semibold mb-3">Offer tracking</h4>
                  {offers.length === 0 ? <p className="text-gray-600">No offers recorded yet.</p> : (
                    <ul className="space-y-2">
                      {offers.map(o => (
                        <li key={o.id} className="p-3 bg-white rounded border flex justify-between">
                          <span className="text-gray-800">{o.user_name || 'Mentee'} — {o.university}</span>
                          <span className="text-xs uppercase text-gray-500">{o.status}</span>
                        </li>
                      ))}
                    </ul>
                  )}
                </div>
              </div>
            )}

            {tab === 'cohorts' && (
              <CohortsPanel
                cohorts={cohorts} newCohort={newCohort} setNewCohort={setNewCohort}
                savingCohort={savingCohort} onCreate={addCohort} onError={setError}
              />
            )}

            {tab === 'resources' && (
              <div>
                <h4 className="text-lg font-semibold mb-3">Add Resource</h4>
                <form onSubmit={addResource} className="space-y-3 mb-6">
                  <input value={newResource.title} onChange={e => setNewResource({...newResource, title: e.target.value})} placeholder="Title" required className="w-full p-2 rounded border" />
                  <input value={newResource.url} onChange={e => setNewResource({...newResource, url: e.target.value})} placeholder="URL" required className="w-full p-2 rounded border" />
                  <select value={newResource.type} onChange={e => setNewResource({...newResource, type: e.target.value})} className="w-full p-2 rounded border">
                    {RESOURCE_TYPES.map(t => <option key={t.value} value={t.value}>{t.label}</option>)}
                  </select>
                  <textarea value={newResource.description} onChange={e => setNewResource({...newResource, description: e.target.value})} placeholder="Description" className="w-full p-2 rounded border" />
                  <button disabled={savingResource} className="px-4 py-2 bg-yellow-600 text-white rounded disabled:opacity-50">
                    {savingResource ? 'Adding...' : 'Add Resource'}
                  </button>
                </form>
                <h4 className="text-lg font-semibold mb-3">Existing Resources</h4>
                {resources.length === 0 ? <p className="text-gray-600">No resources added yet.</p> : (
                  <ul className="space-y-3">
                    {resources.map((r) => (
                      <li key={r.id} className="p-3 bg-white rounded shadow-sm flex justify-between items-start gap-4 border">
                        <div>
                          <a href={r.url || '#'} target="_blank" rel="noreferrer" className="text-yellow-600 font-semibold">{r.title}</a>
                          <span className="ml-2 text-xs uppercase text-gray-400">{r.type}</span>
                          {r.description && <p className="text-gray-600 mt-1">{r.description}</p>}
                        </div>
                        <button onClick={() => deleteResource(r.id)} className="text-sm text-red-600 hover:underline shrink-0">Delete</button>
                      </li>
                    ))}
                  </ul>
                )}
              </div>
            )}

            {tab === 'notifications' && (
              <div>
                <p className="text-gray-600 mb-4 text-sm">Stubbed outbound notifications (the "Mail Merge" log). Emails aren't sent yet — each selection decision records an entry here.</p>
                {notifications.length === 0 ? <p className="text-gray-600">No notifications logged yet.</p> : (
                  <ul className="space-y-3">
                    {notifications.map(n => (
                      <li key={n.id} className="p-3 bg-white rounded shadow-sm border">
                        <div className="flex justify-between">
                          <span className="font-semibold text-gray-800">{n.subject}</span>
                          <span className="text-xs uppercase text-gray-400">{n.template}</span>
                        </div>
                        <p className="text-gray-600 mt-1 text-sm">{n.body}</p>
                      </li>
                    ))}
                  </ul>
                )}
              </div>
            )}
          </div>
        </main>
      </div>
    </div>
  )
}

function PeopleTable({ kind, people, total, page, totalPages, searchInput, setSearchInput, onSearch, onPage }){
  const isMentor = kind === 'mentors'
  return (
    <div>
      <form onSubmit={onSearch} className="flex gap-2 mb-4 max-w-md">
        <input value={searchInput} onChange={e => setSearchInput(e.target.value)}
          placeholder={`Search ${kind} by name or email`} className="flex-1 p-2 rounded border" />
        <button className="px-4 py-2 bg-yellow-600 text-white rounded">Search</button>
      </form>
      <div className="overflow-x-auto rounded-lg border border-gray-200">
        <table className="min-w-full table-auto border-collapse">
          <thead className="bg-gray-50"><tr className="text-left">
            <th className="py-2 px-3">Name</th><th className="py-2 px-3">Email</th><th className="py-2 px-3">Phone</th>
            {isMentor ? (<><th className="py-2 px-3">Discipline</th><th className="py-2 px-3">Expertise</th><th className="py-2 px-3">Availability</th><th className="py-2 px-3">Abroad</th></>)
              : (<><th className="py-2 px-3">Country</th><th className="py-2 px-3">Level</th><th className="py-2 px-3">University</th><th className="py-2 px-3">Course</th></>)}
            <th className="py-2 px-3">Declaration</th><th className="py-2 px-3">Joined</th><th className="py-2 px-3">Status</th>
          </tr></thead>
          <tbody>
            {people.map(u => {
              const p = isMentor ? u.mentor_profile : u.mentee_profile
              return (
                <tr key={u.id} className="border-t hover:bg-yellow-50 align-top">
                  <td className="py-2 px-3">{u.full_name}</td>
                  <td className="py-2 px-3">{u.email}</td>
                  <td className="py-2 px-3">{u.phone || '—'}</td>
                  {isMentor ? (<>
                    <td className="py-2 px-3">{p?.discipline || '—'}</td>
                    <td className="py-2 px-3">{p?.expertise?.length ? p.expertise.join(', ') : '—'}</td>
                    <td className="py-2 px-3">{p?.availability || '—'}</td>
                    <td className="py-2 px-3">{p?.studied_abroad ? 'Yes' : 'No'}</td>
                  </>) : (<>
                    <td className="py-2 px-3">{p?.country || '—'}</td>
                    <td className="py-2 px-3">{p?.level || '—'}</td>
                    <td className="py-2 px-3">{p?.university || '—'}</td>
                    <td className="py-2 px-3">{p?.course || '—'}</td>
                  </>)}
                  <td className="py-2 px-3">{u.declaration_signed_at ? 'Signed' : 'Pending'}</td>
                  <td className="py-2 px-3 text-sm text-gray-500">{u.date_joined ? String(u.date_joined).slice(0, 10) : '—'}</td>
                  <td className="py-2 px-3">{u.is_active ? 'Active' : 'Inactive'}</td>
                </tr>
              )
            })}
            {people.length === 0 && <tr><td colSpan="10" className="py-3 px-3 text-gray-500">No {kind} found.</td></tr>}
          </tbody>
        </table>
      </div>
      <div className="flex items-center justify-between mt-4">
        <p className="text-sm text-gray-600">{total} {kind} total</p>
        <div className="flex items-center gap-3">
          <button onClick={() => onPage(page - 1)} disabled={page <= 0} className="px-3 py-1 rounded border disabled:opacity-40">Prev</button>
          <span className="text-sm text-gray-700">Page {page + 1} of {totalPages}</span>
          <button onClick={() => onPage(page + 1)} disabled={page + 1 >= totalPages} className="px-3 py-1 rounded border disabled:opacity-40">Next</button>
        </div>
      </div>
    </div>
  )
}

function ApplicationsPanel({ board, cohorts, reviewers, boardCohort, onCohortChange, onRunScoring, onAssign, onComputeSystem, onDecision }){
  const [openId, setOpenId] = useState(null)
  const [sel, setSel] = useState({})     // appId -> [reviewerId]
  const [notes, setNotes] = useState({}) // appId -> notes

  function toggleReviewer(appId, rid){
    const cur = sel[appId] || []
    setSel({ ...sel, [appId]: cur.includes(rid) ? cur.filter(x => x !== rid) : [...cur, rid] })
  }

  return (
    <div>
      <div className="flex flex-wrap items-center gap-3 mb-5">
        <select value={boardCohort} onChange={e => onCohortChange(e.target.value)} className="p-2 rounded border">
          <option value="">All cohorts</option>
          {cohorts.map(c => <option key={c.id} value={c.id}>{c.name}</option>)}
        </select>
        <button onClick={onRunScoring} disabled={!boardCohort} className="px-4 py-2 bg-gray-800 text-white rounded disabled:opacity-40">
          Run disadvantage scoring
        </button>
        <span className="text-sm text-gray-500">Pick a cohort to score its applications.</span>
      </div>

      <div className="overflow-x-auto rounded-lg border border-gray-200">
        <table className="min-w-full table-auto border-collapse">
          <thead className="bg-gray-50"><tr className="text-left">
            <th className="py-2 px-3">Applicant</th><th className="py-2 px-3">Score</th>
            <th className="py-2 px-3">Reviews</th><th className="py-2 px-3">System</th>
            <th className="py-2 px-3">Admin</th><th className="py-2 px-3">Status</th><th className="py-2 px-3"></th>
          </tr></thead>
          <tbody>
            {board.map(a => (
              <React.Fragment key={a.id}>
                <tr className="border-t hover:bg-yellow-50 align-top">
                  <td className="py-2 px-3">
                    <div className="font-medium">{a.applicant_name || '—'}</div>
                    <div className="text-xs text-gray-500">{a.applicant_email}</div>
                  </td>
                  <td className="py-2 px-3">{a.disadvantage_score}</td>
                  <td className="py-2 px-3 text-sm">
                    {a.reviews.length ? a.reviews.map((r, i) => (
                      <div key={i}>{r.reviewer_name || 'reviewer'}: <span className="capitalize">{r.decision || 'pending'}</span></div>
                    )) : <span className="text-gray-400">none</span>}
                  </td>
                  <td className="py-2 px-3 capitalize">
                    {a.system_decision || '—'}
                    {a.reconciliation_needed && <span className="ml-1 text-xs px-2 py-0.5 rounded bg-orange-100 text-orange-700">reconcile</span>}
                  </td>
                  <td className="py-2 px-3 capitalize">{a.admin_decision || '—'}</td>
                  <td className="py-2 px-3 capitalize">{String(a.status).replace('_', ' ')}</td>
                  <td className="py-2 px-3">
                    <button onClick={() => setOpenId(openId === a.id ? null : a.id)} className="text-sm text-yellow-700 hover:underline">
                      {openId === a.id ? 'Close' : 'Manage'}
                    </button>
                  </td>
                </tr>
                {openId === a.id && (
                  <tr className="bg-yellow-50/60">
                    <td colSpan="7" className="py-4 px-3">
                      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                        <div>
                          <p className="font-semibold text-gray-700 mb-2">1. Assign reviewers</p>
                          {reviewers.length === 0 ? <p className="text-sm text-gray-500">No users with the reviewer role.</p> : (
                            <div className="space-y-1 max-h-40 overflow-y-auto">
                              {reviewers.map(r => (
                                <label key={r.id} className="flex items-center gap-2 text-sm">
                                  <input type="checkbox" checked={(sel[a.id] || []).includes(r.id)} onChange={() => toggleReviewer(a.id, r.id)} />
                                  {r.full_name} <span className="text-gray-400">{r.email}</span>
                                </label>
                              ))}
                            </div>
                          )}
                          <button onClick={() => onAssign(a.id, sel[a.id] || [])} className="mt-2 px-3 py-1 bg-yellow-600 text-white rounded text-sm">Assign</button>
                        </div>
                        <div>
                          <p className="font-semibold text-gray-700 mb-2">2. System decision</p>
                          <p className="text-sm text-gray-600 mb-2">Applies the threshold + reviewer-majority formula.</p>
                          <button onClick={() => onComputeSystem(a.id)} className="px-3 py-1 bg-gray-800 text-white rounded text-sm">Compute</button>
                        </div>
                        <div>
                          <p className="font-semibold text-gray-700 mb-2">3. Admin decision</p>
                          <input value={notes[a.id] || ''} onChange={e => setNotes({ ...notes, [a.id]: e.target.value })}
                            placeholder="Notes (optional)" className="w-full p-2 rounded border text-sm mb-2" />
                          <div className="flex gap-2">
                            {DECISIONS.map(d => (
                              <button key={d} onClick={() => onDecision(a.id, d, notes[a.id] || null)}
                                className="px-3 py-1 rounded text-sm capitalize border hover:bg-white">{d}</button>
                            ))}
                          </div>
                        </div>
                      </div>
                    </td>
                  </tr>
                )}
              </React.Fragment>
            ))}
            {board.length === 0 && <tr><td colSpan="7" className="py-3 px-3 text-gray-500">No applications.</td></tr>}
          </tbody>
        </table>
      </div>
    </div>
  )
}

function WorkshopsPanel({ workshops, newWorkshop, setNewWorkshop, saving, onCreate, onDelete }){
  return (
    <div>
      <h4 className="text-lg font-semibold mb-3">Create Workshop</h4>
      <form onSubmit={onCreate} className="grid grid-cols-1 sm:grid-cols-2 gap-3 mb-8 max-w-3xl">
        <input value={newWorkshop.title} onChange={e => setNewWorkshop({...newWorkshop, title: e.target.value})} placeholder="Title" required className="p-2 rounded border" />
        <select value={newWorkshop.audience} onChange={e => setNewWorkshop({...newWorkshop, audience: e.target.value})} className="p-2 rounded border">
          <option value="public">Public</option>
          <option value="mentee_only">Mentee only</option>
        </select>
        <label className="text-sm text-gray-600">Date
          <input type="date" value={newWorkshop.scheduled_date} onChange={e => setNewWorkshop({...newWorkshop, scheduled_date: e.target.value})} className="mt-1 w-full p-2 rounded border" />
        </label>
        <input value={newWorkshop.recording_url} onChange={e => setNewWorkshop({...newWorkshop, recording_url: e.target.value})} placeholder="Recording URL (YouTube)" className="p-2 rounded border" />
        <textarea value={newWorkshop.description} onChange={e => setNewWorkshop({...newWorkshop, description: e.target.value})} placeholder="Description" className="p-2 rounded border sm:col-span-2" />
        <div className="sm:col-span-2">
          <button disabled={saving} className="px-4 py-2 bg-yellow-600 text-white rounded disabled:opacity-50">
            {saving ? 'Creating...' : 'Create Workshop'}
          </button>
        </div>
      </form>

      <h4 className="text-lg font-semibold mb-3">Scheduled Workshops</h4>
      {workshops.length === 0 ? <p className="text-gray-600">No workshops yet.</p> : (
        <ul className="space-y-3">
          {workshops.map(w => (
            <li key={w.id} className="p-3 bg-white rounded shadow-sm border flex justify-between items-start gap-4">
              <div>
                <p className="font-semibold text-gray-800">{w.title} <span className="text-xs uppercase text-gray-400">{String(w.audience).replace('_', ' ')}</span></p>
                <p className="text-sm text-gray-500">{w.scheduled_date || 'unscheduled'} · {w.signup_count} panellist(s)</p>
                {w.recording_url && <a href={w.recording_url} target="_blank" rel="noreferrer" className="text-sm text-yellow-600">Recording</a>}
                {w.description && <p className="text-gray-600 mt-1 text-sm">{w.description}</p>}
              </div>
              <button onClick={() => onDelete(w.id)} className="text-sm text-red-600 hover:underline shrink-0">Delete</button>
            </li>
          ))}
        </ul>
      )}
    </div>
  )
}

function DocumentsPanel({ documents, mentors, onAssign }){
  const [pick, setPick] = useState({}) // docId -> mentorId
  return (
    <div className="overflow-x-auto rounded-lg border border-gray-200">
      <table className="min-w-full table-auto border-collapse">
        <thead className="bg-gray-50"><tr className="text-left">
          <th className="py-2 px-3">Document</th><th className="py-2 px-3">Applicant</th>
          <th className="py-2 px-3">Status</th><th className="py-2 px-3">Reviewer</th>
          <th className="py-2 px-3">Assign / Feedback</th>
        </tr></thead>
        <tbody>
          {documents.map(d => (
            <tr key={d.id} className="border-t hover:bg-yellow-50 align-top">
              <td className="py-2 px-3"><a href={d.url} target="_blank" rel="noreferrer" className="text-yellow-600 font-medium">{d.title}</a><div className="text-xs text-gray-400">{d.doc_type}</div></td>
              <td className="py-2 px-3">{d.applicant_name || '—'}</td>
              <td className="py-2 px-3 capitalize">{String(d.status).replace('_', ' ')}</td>
              <td className="py-2 px-3">{d.reviewer_name || '—'}</td>
              <td className="py-2 px-3">
                <div className="flex gap-2 items-center">
                  <select value={pick[d.id] || ''} onChange={e => setPick({ ...pick, [d.id]: e.target.value })} className="p-1 rounded border text-sm">
                    <option value="">Reviewer…</option>
                    {mentors.map(m => <option key={m.id} value={m.id}>{m.full_name}</option>)}
                  </select>
                  <button onClick={() => onAssign(d.id, pick[d.id])} className="px-2 py-1 bg-yellow-600 text-white rounded text-sm">Assign</button>
                </div>
                {d.feedback && <p className="mt-1 text-xs text-gray-600">“{d.feedback}”</p>}
              </td>
            </tr>
          ))}
          {documents.length === 0 && <tr><td colSpan="5" className="py-3 px-3 text-gray-500">No documents submitted yet.</td></tr>}
        </tbody>
      </table>
    </div>
  )
}

function MappingPanel({ mapping, cohorts, mappingCohort, onCohortChange, onSetType, onAssign }){
  const [pick, setPick] = useState({}) // menteeUserId -> mentorUserId
  const mentors = mapping.mentors || []
  const mentorLabel = (m) => `${m.name} — ${m.discipline || 'no discipline'} (${m.assigned}/${m.max_mentees})`

  return (
    <div>
      <div className="flex flex-wrap items-center gap-3 mb-5">
        <select value={mappingCohort} onChange={e => onCohortChange(e.target.value)} className="p-2 rounded border">
          <option value="">All cohorts</option>
          {cohorts.map(c => <option key={c.id} value={c.id}>{c.name}</option>)}
        </select>
        <span className="text-sm text-gray-500">Assign mentorship type, then pair one-on-one mentees with a mentor.</span>
      </div>

      <div className="overflow-x-auto rounded-lg border border-gray-200">
        <table className="min-w-full table-auto border-collapse">
          <thead className="bg-gray-50"><tr className="text-left">
            <th className="py-2 px-3">Mentee</th><th className="py-2 px-3">Discipline</th>
            <th className="py-2 px-3">Score</th><th className="py-2 px-3">Type</th>
            <th className="py-2 px-3">Current mentor</th><th className="py-2 px-3">Assign mentor (one-on-one)</th>
          </tr></thead>
          <tbody>
            {mapping.mentees.map(m => {
              const suggested = new Set(m.suggested_mentor_ids || [])
              const options = [...mentors].sort((a, b) => (suggested.has(b.user_id) ? 1 : 0) - (suggested.has(a.user_id) ? 1 : 0))
              return (
                <tr key={m.user_id} className="border-t hover:bg-yellow-50 align-top">
                  <td className="py-2 px-3">{m.name}</td>
                  <td className="py-2 px-3">{m.discipline || '—'}</td>
                  <td className="py-2 px-3">{m.disadvantage_score}</td>
                  <td className="py-2 px-3">
                    <div className="flex gap-1">
                      {['one_on_one', 'cohort'].map(t => (
                        <button key={t} onClick={() => onSetType(m.user_id, t)}
                          className={`px-2 py-1 rounded text-xs border ${m.mentorship_type === t ? 'bg-yellow-600 text-white' : 'hover:bg-white'}`}>
                          {t === 'one_on_one' ? '1:1' : 'cohort'}
                        </button>
                      ))}
                    </div>
                  </td>
                  <td className="py-2 px-3">{m.current_mentor_name || '—'}</td>
                  <td className="py-2 px-3">
                    <div className="flex gap-2 items-center">
                      <select value={pick[m.user_id] || ''} onChange={e => setPick({ ...pick, [m.user_id]: e.target.value })} className="p-1 rounded border text-sm">
                        <option value="">Select mentor…</option>
                        {options.map(mt => (
                          <option key={mt.user_id} value={mt.user_id}>
                            {suggested.has(mt.user_id) ? '★ ' : ''}{mentorLabel(mt)}
                          </option>
                        ))}
                      </select>
                      <button onClick={() => onAssign(m.user_id, pick[m.user_id], m.cohort_id)} className="px-3 py-1 bg-yellow-600 text-white rounded text-sm">Pair</button>
                    </div>
                  </td>
                </tr>
              )
            })}
            {mapping.mentees.length === 0 && <tr><td colSpan="6" className="py-3 px-3 text-gray-500">No mentees to map.</td></tr>}
          </tbody>
        </table>
      </div>
      <p className="text-xs text-gray-500 mt-2">★ = same-discipline mentor with remaining capacity.</p>
    </div>
  )
}

function CohortsPanel({ cohorts, newCohort, setNewCohort, savingCohort, onCreate, onError }){
  const [formCohort, setFormCohort] = useState('')
  const [fields, setFields] = useState([])
  const [newField, setNewField] = useState(EMPTY_FIELD)

  async function loadFields(cohortId){
    if (!cohortId) { setFields([]); return }
    try { setFields((await api.get(`/api/cohorts/${cohortId}/form-configs`)).data) }
    catch (err) { onError(errText(err, 'Failed to load form fields.')) }
  }
  async function addField(e){
    e.preventDefault()
    if (!formCohort || !newField.field_name) return
    try {
      await api.post('/api/form-configs', {
        cohort_id: formCohort,
        field_name: newField.field_name,
        field_type: newField.field_type,
        is_required: newField.is_required,
        field_order: Number(newField.field_order) || 0,
        options: newField.options ? newField.options.split(',').map(s => s.trim()).filter(Boolean) : [],
      })
      setNewField(EMPTY_FIELD); await loadFields(formCohort)
    } catch (err) { onError(errText(err, 'Failed to add field.')) }
  }
  async function deleteField(id){
    try { await api.delete(`/api/form-configs/${id}`); await loadFields(formCohort) }
    catch (err) { onError(errText(err, 'Failed to delete field.')) }
  }

  return (
    <div>
      <h4 className="text-lg font-semibold mb-3">Create Cohort</h4>
      <form onSubmit={onCreate} className="grid grid-cols-1 sm:grid-cols-2 gap-3 mb-8 max-w-3xl">
        <input value={newCohort.name} onChange={e => setNewCohort({...newCohort, name: e.target.value})} placeholder="Name" required className="p-2 rounded border" />
        <input value={newCohort.program} onChange={e => setNewCohort({...newCohort, program: e.target.value})} placeholder="Program" required className="p-2 rounded border" />
        <label className="text-sm text-gray-600">Start date
          <input type="date" value={newCohort.start_date} onChange={e => setNewCohort({...newCohort, start_date: e.target.value})} required className="mt-1 w-full p-2 rounded border" />
        </label>
        <label className="text-sm text-gray-600">End date
          <input type="date" value={newCohort.end_date} onChange={e => setNewCohort({...newCohort, end_date: e.target.value})} required className="mt-1 w-full p-2 rounded border" />
        </label>
        <select value={newCohort.status} onChange={e => setNewCohort({...newCohort, status: e.target.value})} className="p-2 rounded border">
          {COHORT_STATUSES.map(s => <option key={s} value={s}>{s}</option>)}
        </select>
        <input type="number" min="1" value={newCohort.max_mentees} onChange={e => setNewCohort({...newCohort, max_mentees: e.target.value})} placeholder="Max mentees" required className="p-2 rounded border" />
        <label className="text-sm text-gray-600">Selection threshold (disadvantage score)
          <input type="number" step="0.1" value={newCohort.selection_threshold} onChange={e => setNewCohort({...newCohort, selection_threshold: e.target.value})} className="mt-1 w-full p-2 rounded border" />
        </label>
        <div className="sm:col-span-2">
          <button disabled={savingCohort} className="px-4 py-2 bg-yellow-600 text-white rounded disabled:opacity-50">
            {savingCohort ? 'Creating...' : 'Create Cohort'}
          </button>
        </div>
      </form>

      <h4 className="text-lg font-semibold mb-3">Existing Cohorts</h4>
      <div className="overflow-x-auto rounded-lg border border-gray-200 mb-10">
        <table className="min-w-full table-auto border-collapse">
          <thead className="bg-gray-50"><tr className="text-left">
            <th className="py-3 px-4">Name</th><th className="py-3 px-4">Program</th><th className="py-3 px-4">Dates</th>
            <th className="py-3 px-4">Status</th><th className="py-3 px-4">Max</th><th className="py-3 px-4">Threshold</th>
          </tr></thead>
          <tbody>
            {cohorts.map(c => (
              <tr key={c.id} className="border-t hover:bg-yellow-50">
                <td className="py-3 px-4 font-medium">{c.name}</td>
                <td className="py-3 px-4">{c.program}</td>
                <td className="py-3 px-4 text-sm text-gray-600">{c.start_date} → {c.end_date}</td>
                <td className="py-3 px-4 capitalize">{c.status}</td>
                <td className="py-3 px-4">{c.max_mentees}</td>
                <td className="py-3 px-4">{c.selection_threshold}</td>
              </tr>
            ))}
            {cohorts.length === 0 && <tr><td colSpan="6" className="py-3 px-4 text-gray-500">No cohorts yet.</td></tr>}
          </tbody>
        </table>
      </div>

      <h4 className="text-lg font-semibold mb-3">Application Form Builder</h4>
      <div className="mb-3 max-w-md">
        <select value={formCohort} onChange={e => { setFormCohort(e.target.value); loadFields(e.target.value) }} className="w-full p-2 rounded border">
          <option value="">Select a cohort to configure its form</option>
          {cohorts.map(c => <option key={c.id} value={c.id}>{c.name}</option>)}
        </select>
      </div>

      {formCohort && (
        <>
          {fields.length === 0 ? <p className="text-gray-600 mb-3">No custom fields — applicants see the default questions only.</p> : (
            <ul className="space-y-2 mb-4">
              {fields.map(f => (
                <li key={f.id} className="p-2 bg-white rounded border flex justify-between items-center text-sm">
                  <span>#{f.field_order} <span className="font-medium">{f.field_name}</span> <span className="text-gray-400">({f.field_type}{f.is_required ? ', required' : ''})</span></span>
                  <button onClick={() => deleteField(f.id)} className="text-red-600 hover:underline">Delete</button>
                </li>
              ))}
            </ul>
          )}
          <form onSubmit={addField} className="grid grid-cols-1 sm:grid-cols-2 gap-3 max-w-3xl">
            <input value={newField.field_name} onChange={e => setNewField({...newField, field_name: e.target.value})} placeholder="Field name" required className="p-2 rounded border" />
            <select value={newField.field_type} onChange={e => setNewField({...newField, field_type: e.target.value})} className="p-2 rounded border">
              {FIELD_TYPES.map(t => <option key={t} value={t}>{t}</option>)}
            </select>
            <input value={newField.options} onChange={e => setNewField({...newField, options: e.target.value})} placeholder="Options (comma-separated, for dropdown)" className="p-2 rounded border" />
            <input type="number" value={newField.field_order} onChange={e => setNewField({...newField, field_order: e.target.value})} placeholder="Order" className="p-2 rounded border" />
            <label className="flex items-center gap-2 text-sm text-gray-700">
              <input type="checkbox" checked={newField.is_required} onChange={e => setNewField({...newField, is_required: e.target.checked})} /> Required
            </label>
            <div className="sm:col-span-2">
              <button className="px-4 py-2 bg-yellow-600 text-white rounded">Add field</button>
            </div>
          </form>
        </>
      )}
    </div>
  )
}
