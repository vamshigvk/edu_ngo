import React, { useEffect, useState } from 'react'
import api from '../../services/api'

// Shared workshops list for mentor/mentee dashboards. Mentors can sign up as
// panellists (canSignup); everyone sees recordings + schedule.
export default function WorkshopsSection({ canSignup = false }){
  const [workshops, setWorkshops] = useState([])
  const [msg, setMsg] = useState('')

  async function load(){
    try { setWorkshops((await api.get('/api/workshops')).data) } catch { /* ignore */ }
  }
  useEffect(() => { load() }, [])

  async function signup(id){
    setMsg('')
    try { await api.post(`/api/workshops/${id}/signup`); setMsg('You are signed up as a panellist.'); await load() }
    catch (err) { setMsg(err?.response?.data?.error?.message || 'Could not sign up.') }
  }

  return (
    <section className="mb-10">
      <h2 className="text-xl font-semibold text-gray-800 mb-3">Workshops</h2>
      {msg && <p className="text-sm text-gray-600 mb-2">{msg}</p>}
      {workshops.length === 0 ? <p className="text-gray-600">No workshops scheduled yet.</p> : (
        <ul className="space-y-2">
          {workshops.map(w => (
            <li key={w.id} className="p-4 bg-white rounded shadow-sm border flex justify-between items-start gap-4">
              <div>
                <p className="font-medium text-gray-800">{w.title} <span className="text-xs uppercase text-gray-400">{String(w.audience).replace('_', ' ')}</span></p>
                <p className="text-sm text-gray-500">{w.scheduled_date || 'unscheduled'}</p>
                {w.recording_url && <a href={w.recording_url} target="_blank" rel="noreferrer" className="text-sm text-yellow-600">Watch recording</a>}
                {w.description && <p className="text-gray-600 mt-1 text-sm">{w.description}</p>}
              </div>
              {canSignup && (
                <button onClick={() => signup(w.id)} className="px-3 py-1 bg-yellow-600 text-white rounded text-sm shrink-0">
                  Sign up as panellist
                </button>
              )}
            </li>
          ))}
        </ul>
      )}
    </section>
  )
}
