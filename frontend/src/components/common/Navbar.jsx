import React from 'react'
import { Link } from 'react-router-dom'

export default function Navbar(){
  return (
    <nav className="bg-black shadow-sm">
      <div className="max-w-6xl mx-auto px-4 py-4 flex items-center justify-between">
        <Link to="/" className="text-2xl font-bold text-yellow-400">ProjectEduAccess</Link>
        <div className="hidden md:flex space-x-8">
          <Link to="/" className="text-yellow-400 hover:text-yellow-300 font-semibold">Home</Link>
          <Link to="/about" className="text-yellow-400 hover:text-yellow-300 font-semibold">About Us</Link>
          <Link to="/work" className="text-yellow-400 hover:text-yellow-300 font-semibold">Our Work</Link>
          <Link to="/apply" className="text-yellow-400 hover:text-yellow-300 font-semibold">Apply</Link>
          <Link to="/resources" className="text-yellow-400 hover:text-yellow-300 font-semibold">Resources</Link>
          <Link to="/login" className="text-yellow-400 hover:text-yellow-300 font-semibold">Login</Link>
        </div>
        <div className="md:hidden text-yellow-400">Menu</div>
      </div>
    </nav>
  )
}
