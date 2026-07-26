import React from 'react'

export default function Footer() {
  return (
    <footer className="bg-black border-t-4 border-yellow-400">
      <div className="max-w-6xl mx-auto px-4 py-8 text-sm text-yellow-400">
        <div className="flex justify-between">
          <div>
            <h4 className="font-semibold text-yellow-400 text-lg">ProjectEduAccess</h4>
            <p className="mt-1">Democratising access to education & opportunities.</p>
          </div>
          <div>
            <p>© {new Date().getFullYear()} ProjectEduAccess</p>
          </div>
        </div>
      </div>
    </footer>
  )
}
