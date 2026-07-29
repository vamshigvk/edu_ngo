import React, { useState } from 'react'

// Onboarding gate: a mentor/mentee formally joins the programme only once they
// sign their declaration. Shows a prompt until signed, then a confirmation.
export default function DeclarationBanner({ user, signDeclaration, role }){
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState('')

  if (user?.declaration_signed_at) {
    return (
      <div className="mb-6 p-3 bg-green-50 border border-green-300 text-green-800 rounded text-sm">
        ✓ {role.charAt(0).toUpperCase() + role.slice(1)} declaration signed on{' '}
        {String(user.declaration_signed_at).slice(0, 10)}.
      </div>
    )
  }

  async function sign(){
    setSaving(true); setError('')
    try {
      await signDeclaration()
    } catch {
      setError('Could not record your declaration. Please try again.')
    } finally {
      setSaving(false)
    }
  }

  return (
    <div className="mb-6 p-4 bg-yellow-100 border border-yellow-400 rounded">
      <p className="text-gray-800 font-medium">Confirm your participation</p>
      <p className="text-gray-700 text-sm mt-1">
        You've been selected. Please sign the {role} declaration to confirm you'll
        take part in the mentorship programme this cycle.
      </p>
      {error && <p className="text-red-700 text-sm mt-2">{error}</p>}
      <button
        onClick={sign}
        disabled={saving}
        className="mt-3 px-4 py-2 bg-black text-yellow-400 font-semibold rounded hover:bg-gray-900 disabled:opacity-50"
      >
        {saving ? 'Signing...' : 'Sign declaration'}
      </button>
    </div>
  )
}
