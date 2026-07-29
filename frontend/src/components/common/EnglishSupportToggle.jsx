import React, { useState } from 'react'
import api from '../../services/api'

// Self-serve opt-in for the English Language Support Programme (Phase 5).
export default function EnglishSupportToggle({ initial }){
  const [optedIn, setOptedIn] = useState(!!initial)
  const [saving, setSaving] = useState(false)

  async function toggle(){
    const next = !optedIn
    setSaving(true)
    try {
      await api.post('/auth/english-support', { opt_in: next })
      setOptedIn(next)
    } catch { /* leave state unchanged */ } finally { setSaving(false) }
  }

  return (
    <label className="flex items-center gap-2 text-sm text-gray-700">
      <input type="checkbox" checked={optedIn} onChange={toggle} disabled={saving} />
      Opt in to the English Language Support Programme
    </label>
  )
}
