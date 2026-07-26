import React from 'react'
import { Link } from 'react-router-dom'

export default function Apply(){
  return (
    <div className="max-w-4xl mx-auto px-4 py-12">
      <h1 className="text-3xl font-bold text-black">Apply</h1>
      <p className="mt-4 text-gray-800 text-lg">Student and Mentor application forms will be available here.</p>

      <div className="mt-8 flex gap-4">
        <Link to="/apply/student" className="px-6 py-3 bg-black text-yellow-400 font-semibold rounded hover:bg-gray-900">Apply as Student</Link>
        <Link to="/apply/mentor" className="px-6 py-3 bg-black text-yellow-400 font-semibold rounded hover:bg-gray-900">Become a Mentor</Link>
      </div>
    </div>
  )
}
