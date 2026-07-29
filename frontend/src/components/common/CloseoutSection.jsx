import React, { useState } from 'react'
import api from '../../services/api'

// End-of-cycle actions for a mentee: feedback, offer tracking, and the option
// to return next cycle as a mentor (alumni).
export default function CloseoutSection(){
  const [feedback, setFeedback] = useState({ rating: 5, comments: '' })
  const [offer, setOffer] = useState({ university: '', status: 'applied' })
  const [msg, setMsg] = useState('')
  const [busy, setBusy] = useState(false)

  async function submitFeedback(e){
    e.preventDefault(); setMsg('')
    try { await api.post('/api/closeout/feedback', feedback); setMsg('Thanks for your feedback!'); setFeedback({ rating: 5, comments: '' }) }
    catch (err) { setMsg(err?.response?.data?.error?.message || 'Could not submit feedback.') }
  }
  async function submitOffer(e){
    e.preventDefault(); setMsg('')
    if (!offer.university) return
    try { await api.post('/api/closeout/offers', offer); setMsg('Offer recorded.'); setOffer({ university: '', status: 'applied' }) }
    catch (err) { setMsg(err?.response?.data?.error?.message || 'Could not record offer.') }
  }
  async function becomeMentor(){
    setBusy(true); setMsg('')
    try {
      const { data } = await api.post('/api/closeout/become-mentor')
      localStorage.setItem('user', JSON.stringify(data))
      window.location.href = '/mentor'  // reload so the app picks up the new role
    } catch (err) {
      setMsg(err?.response?.data?.error?.message || 'Could not switch to mentor.')
      setBusy(false)
    }
  }

  return (
    <section className="mb-10">
      <h2 className="text-xl font-semibold text-gray-800 mb-3">Close of programme</h2>
      {msg && <p className="text-sm text-gray-600 mb-3">{msg}</p>}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <form onSubmit={submitFeedback} className="p-4 bg-white rounded border space-y-3">
          <h3 className="font-semibold text-gray-800">Programme feedback</h3>
          <label className="block text-sm text-gray-600">Rating (1-5)
            <input type="number" min="1" max="5" value={feedback.rating}
              onChange={e => setFeedback({ ...feedback, rating: Number(e.target.value) })}
              className="mt-1 w-full p-2 rounded border" />
          </label>
          <textarea value={feedback.comments} onChange={e => setFeedback({ ...feedback, comments: e.target.value })}
            placeholder="What worked well? What could improve?" rows="3" className="w-full p-2 rounded border" />
          <button className="px-4 py-2 bg-yellow-600 text-white rounded">Submit feedback</button>
        </form>

        <form onSubmit={submitOffer} className="p-4 bg-white rounded border space-y-3">
          <h3 className="font-semibold text-gray-800">Offer tracking</h3>
          <input value={offer.university} onChange={e => setOffer({ ...offer, university: e.target.value })}
            placeholder="University / programme" required className="w-full p-2 rounded border" />
          <select value={offer.status} onChange={e => setOffer({ ...offer, status: e.target.value })} className="w-full p-2 rounded border">
            <option value="applied">Applied</option>
            <option value="admitted">Admitted</option>
            <option value="scholarship">Scholarship</option>
            <option value="rejected">Rejected</option>
          </select>
          <button className="px-4 py-2 bg-yellow-600 text-white rounded">Record offer</button>
        </form>
      </div>

      <div className="mt-6 p-4 bg-yellow-50 border border-yellow-300 rounded">
        <p className="text-gray-800 font-medium">Give back next cycle</p>
        <p className="text-gray-700 text-sm mt-1">Moving on? Return as a mentor and join the alumni network.</p>
        <button onClick={becomeMentor} disabled={busy} className="mt-3 px-4 py-2 bg-black text-yellow-400 font-semibold rounded hover:bg-gray-900 disabled:opacity-50">
          {busy ? 'Switching…' : 'Become a mentor'}
        </button>
      </div>
    </section>
  )
}
