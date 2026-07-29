import React, { useContext } from 'react'
import { Link } from 'react-router-dom'
import { AuthContext } from '../../context/AuthContext'

const DASHBOARD_FOR_ROLE = {
  admin: '/admin',
  mentor: '/mentor',
  mentee: '/mentee',
  reviewer: '/review',
}

export default function Navbar(){
  const { user, logout } = useContext(AuthContext)
  const linkClass = 'text-yellow-400 hover:text-yellow-300 font-semibold'

  return (
    <nav className="bg-black shadow-sm">
      <div className="max-w-6xl mx-auto px-4 py-4 flex items-center justify-between">
        <Link to="/" className="text-2xl font-bold text-yellow-400">ProjectEduAccess</Link>
        <div className="hidden md:flex items-center space-x-8">
          <Link to="/" className={linkClass}>Home</Link>
          <Link to="/about" className={linkClass}>About Us</Link>
          <Link to="/work" className={linkClass}>Our Work</Link>
          <Link to="/apply" className={linkClass}>Apply</Link>
          <Link to="/resources" className={linkClass}>Resources</Link>

          {user ? (
            <>
              <Link to={DASHBOARD_FOR_ROLE[user.role] || '/'} className={linkClass}>
                Dashboard
              </Link>
              <span className="text-yellow-200 text-sm">
                {user.full_name} <span className="uppercase text-yellow-500">({user.role})</span>
              </span>
              <button
                onClick={logout}
                className="px-3 py-1 bg-yellow-400 text-black font-semibold rounded hover:bg-yellow-300"
              >
                Logout
              </button>
            </>
          ) : (
            <Link to="/login" className={linkClass}>Login</Link>
          )}
        </div>
        <div className="md:hidden text-yellow-400">Menu</div>
      </div>
    </nav>
  )
}
