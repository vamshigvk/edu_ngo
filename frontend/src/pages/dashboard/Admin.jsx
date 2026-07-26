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

const EMPTY_RESOURCE = { title: '', url: '', type: 'guide', description: '' }

export default function Admin(){
  const { logout } = useContext(AuthContext)
  const [tab, setTab] = useState('mentors')

  const [users, setUsers] = useState([])
  const [pairs, setPairs] = useState([])
  const [resources, setResources] = useState([])
  const [summary, setSummary] = useState(null)
  const [error, setError] = useState('')

  const [newResource, setNewResource] = useState(EMPTY_RESOURCE)
  const [savingResource, setSavingResource] = useState(false)

  const mentors = users.filter(u => u.role === 'mentor')
  const students = users.filter(u => u.role === 'mentee')

  async function loadResources(){
    const { data } = await api.get('/api/resources', { params: { limit: 1000 } })
    setResources(data)
  }

  useEffect(() => {
    async function load(){
      try {
        const [usersRes, pairsRes, dashRes] = await Promise.all([
          api.get('/api/users', { params: { limit: 1000 } }),
          api.get('/api/pairs', { params: { limit: 1000 } }),
          api.get('/dashboard/emp'),
        ])
        setUsers(usersRes.data)
        setPairs(pairsRes.data)
        setSummary(dashRes.data.platform_summary)
        await loadResources()
      } catch (err) {
        const detail = err?.response?.data?.detail
        setError(typeof detail === 'string' ? detail : 'Failed to load dashboard data.')
      }
    }
    load()
  }, [])

  async function addResource(e){
    e.preventDefault()
    if(!newResource.title || !newResource.url) return
    setSavingResource(true)
    setError('')
    try {
      await api.post('/api/resources', newResource)
      setNewResource(EMPTY_RESOURCE)
      await loadResources()
    } catch (err) {
      const detail = err?.response?.data?.detail
      setError(typeof detail === 'string' ? detail : 'Failed to add resource.')
    } finally {
      setSavingResource(false)
    }
  }

  async function deleteResource(id){
    try {
      await api.delete(`/api/resources/${id}`)
      await loadResources()
    } catch (err) {
      const detail = err?.response?.data?.detail
      setError(typeof detail === 'string' ? detail : 'Failed to delete resource.')
    }
  }

  const heading = tab === 'mentors' ? 'Mentors'
    : tab === 'students' ? 'Students'
    : tab === 'matches' ? 'Mentor - Mentee Matches'
    : 'Resources'

  return (
    <div className="min-h-screen bg-yellow-50">
      <div className="min-h-screen flex flex-col md:flex-row">
        <aside className="md:w-72 w-full bg-gray-900 text-yellow-300 p-6 md:min-h-screen">
          <div className="flex items-center justify-between md:block mb-6">
            <h2 className="text-2xl font-semibold">Admin</h2>
            <button onClick={logout} className="px-3 py-2 bg-red-600 rounded text-white md:hidden">Logout</button>
          </div>
          <nav className="space-y-2">
            <button onClick={() => setTab('mentors')} className={`w-full text-left px-3 py-3 rounded ${tab==='mentors' ? 'bg-yellow-700 text-white' : 'hover:bg-yellow-900'}`}>Mentors</button>
            <button onClick={() => setTab('students')} className={`w-full text-left px-3 py-3 rounded ${tab==='students' ? 'bg-yellow-700 text-white' : 'hover:bg-yellow-900'}`}>Students</button>
            <button onClick={() => setTab('matches')} className={`w-full text-left px-3 py-3 rounded ${tab==='matches' ? 'bg-yellow-700 text-white' : 'hover:bg-yellow-900'}`}>Mentor - Mentee Matches</button>
            <button onClick={() => setTab('resources')} className={`w-full text-left px-3 py-3 rounded ${tab==='resources' ? 'bg-yellow-700 text-white' : 'hover:bg-yellow-900'}`}>Resources</button>
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

            {error && (
              <div className="mb-6 p-3 bg-red-100 border border-red-400 text-red-700 rounded">{error}</div>
            )}

            {tab === 'mentors' && (
              <table className="w-full table-auto border-collapse">
                <thead>
                  <tr className="text-left border-b">
                    <th className="py-2">Name</th>
                    <th className="py-2">Email</th>
                    <th className="py-2">Status</th>
                  </tr>
                </thead>
                <tbody>
                  {mentors.map(m => (
                    <tr key={m.id} className="border-b hover:bg-yellow-50">
                      <td className="py-2">{m.full_name}</td>
                      <td className="py-2">{m.email}</td>
                      <td className="py-2">{m.is_active ? 'Active' : 'Inactive'}</td>
                    </tr>
                  ))}
                  {mentors.length === 0 && <tr><td colSpan="3" className="py-3 text-gray-500">No mentors yet.</td></tr>}
                </tbody>
              </table>
            )}

            {tab === 'students' && (
              <table className="w-full table-auto border-collapse">
                <thead>
                  <tr className="text-left border-b">
                    <th className="py-2">Name</th>
                    <th className="py-2">Email</th>
                    <th className="py-2">Status</th>
                  </tr>
                </thead>
                <tbody>
                  {students.map(s => (
                    <tr key={s.id} className="border-b hover:bg-yellow-50">
                      <td className="py-2">{s.full_name}</td>
                      <td className="py-2">{s.email}</td>
                      <td className="py-2">{s.is_active ? 'Active' : 'Inactive'}</td>
                    </tr>
                  ))}
                  {students.length === 0 && <tr><td colSpan="3" className="py-3 text-gray-500">No students yet.</td></tr>}
                </tbody>
              </table>
            )}

            {tab === 'matches' && (
              <div className="overflow-x-auto rounded-lg border border-gray-200">
                <table className="min-w-full table-auto border-collapse">
                  <thead className="bg-gray-50">
                    <tr className="text-left">
                      <th className="py-3 px-4">Mentor</th>
                      <th className="py-3 px-4">Student</th>
                      <th className="py-3 px-4">Status</th>
                      <th className="py-3 px-4">Match Score</th>
                    </tr>
                  </thead>
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
                {resources.length === 0 ? (
                  <p className="text-gray-600">No resources added yet.</p>
                ) : (
                  <ul className="space-y-3">
                    {resources.map((r) => (
                      <li key={r.id} className="p-3 bg-white rounded shadow-sm flex justify-between items-start gap-4">
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
          </div>
        </main>
      </div>
    </div>
  )
}
