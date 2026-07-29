import React, { useEffect, useState } from 'react'
import api from '../../services/api'

export default function Resources(){
  const [resources, setResources] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    async function load(){
      try {
        const { data } = await api.get('/api/public/resources', { params: { limit: 1000 } })
        setResources(data)
      } catch {
        setError('Could not load resources right now.')
      } finally {
        setLoading(false)
      }
    }
    load()
  }, [])

  return (
    <div className="py-12 px-4 max-w-4xl mx-auto">
      <h1 className="text-3xl font-bold text-gray-800 mb-6">Resources</h1>
      {error && <p className="text-red-600">{error}</p>}
      {loading ? (
        <p className="text-gray-600">Loading...</p>
      ) : resources.length === 0 ? (
        <p className="text-gray-600">No resources available yet.</p>
      ) : (
        <ul className="space-y-4">
          {resources.map((r) => (
            <li key={r.id} className="p-4 bg-white rounded shadow-sm">
              <a href={r.url || '#'} className="text-yellow-600 font-semibold" target="_blank" rel="noreferrer">{r.title}</a>
              <span className="ml-2 text-xs uppercase text-gray-400">{r.type}</span>
              {r.description && <p className="text-gray-600 mt-1">{r.description}</p>}
            </li>
          ))}
        </ul>
      )}
    </div>
  )
}
