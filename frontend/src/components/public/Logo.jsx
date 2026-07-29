import React from 'react'
import { Link } from 'react-router-dom'

// Two-line wordmark matching projecteduaccess.com: "project" over "edu access",
// with "edu" in yellow and short yellow blocks trailing each line.
export default function Logo({ className = '' }) {
  return (
    <Link to="/" className={`inline-block leading-none select-none ${className}`} aria-label="Project EduAccess home">
      <div className="flex items-center gap-2">
        <span className="text-2xl font-extrabold tracking-tight text-white">project</span>
        <span className="h-4 w-8 bg-yellow-400" />
      </div>
      <div className="mt-1 flex items-center gap-2">
        <span className="text-2xl font-extrabold tracking-tight">
          <span className="text-yellow-400">edu</span>
          <span className="text-white">access</span>
        </span>
        <span className="h-4 w-6 bg-yellow-400" />
      </div>
    </Link>
  )
}
