import React, { useContext, useState } from 'react'
import { Link, NavLink } from 'react-router-dom'
import Logo from './Logo'
import { AuthContext } from '../../context/AuthContext'

// Navigation mirrors projecteduaccess.com (lowercase, letter-spaced) with the
// same dropdown groupings. Login / Dashboard are our platform additions.
const NAV = [
  { label: 'home', to: '/' },
  {
    label: 'about us',
    to: '/about-us',
    children: [
      { label: 'our approach', to: '/our-approach' },
      { label: 'our team', to: '/team' },
    ],
  },
  {
    label: 'our work',
    to: '/our-work',
    children: [
      { label: 'india', to: '/india' },
      { label: 'afghanistan', to: '/afghanistan' },
      { label: 'sri lanka', to: '/sri-lanka' },
    ],
  },
  { label: 'advocacy', to: '/advocacy' },
  {
    label: 'resources',
    to: '/resources',
    children: [
      { label: 'guides on application documents', to: '/resources/guides' },
      { label: 'resources from online workshops', to: '/resources/workshops' },
      { label: 'kashmir workshop resources', to: '/resources/kashmir' },
    ],
  },
  { label: 'contact us', to: '/contact-us' },
]

const DASHBOARD_FOR_ROLE = { admin: '/admin', mentor: '/mentor', mentee: '/mentee', reviewer: '/review' }
const linkBase = 'text-[13px] uppercase tracking-widest transition'

function DesktopItem({ item }) {
  if (!item.children) {
    return (
      <NavLink
        to={item.to}
        end={item.to === '/'}
        className={({ isActive }) =>
          `${linkBase} ${isActive ? 'text-white' : 'text-neutral-400 hover:text-yellow-400'}`
        }
      >
        {item.label}
      </NavLink>
    )
  }
  return (
    <div className="relative group">
      <NavLink
        to={item.to}
        className={({ isActive }) =>
          `${linkBase} ${isActive ? 'text-white' : 'text-neutral-400 group-hover:text-yellow-400'}`
        }
      >
        {item.label}
      </NavLink>
      <div className="invisible opacity-0 group-hover:visible group-hover:opacity-100 transition absolute left-1/2 -translate-x-1/2 top-full pt-3 z-30">
        <div className="min-w-[220px] bg-neutral-950 border border-yellow-400/30 rounded-md py-2 shadow-xl">
          {item.children.map((c) => (
            <Link
              key={c.to}
              to={c.to}
              className="block px-4 py-2 text-[12px] lowercase text-neutral-300 hover:text-yellow-400 hover:bg-yellow-400/5"
            >
              {c.label}
            </Link>
          ))}
        </div>
      </div>
    </div>
  )
}

export default function PublicHeader() {
  const { user, logout } = useContext(AuthContext)
  const [open, setOpen] = useState(false)

  return (
    <header className="bg-black border-b border-yellow-400/20 sticky top-0 z-40">
      <div className="max-w-6xl mx-auto px-4">
        {/* top row: nav (desktop) + auth actions */}
        <div className="hidden md:flex items-center justify-center gap-8 pt-5">
          {NAV.map((item) => (
            <DesktopItem key={item.to} item={item} />
          ))}
        </div>

        {/* logo + auth actions row */}
        <div className="flex items-center justify-between py-4">
          <Logo />
          <div className="hidden md:flex items-center gap-4">
            {user ? (
              <>
                <Link to={DASHBOARD_FOR_ROLE[user.role] || '/'} className={`${linkBase} text-yellow-400 hover:text-yellow-300`}>
                  dashboard
                </Link>
                <button
                  onClick={logout}
                  className="px-4 py-2 bg-yellow-400 text-black text-[12px] uppercase tracking-widest font-semibold rounded hover:bg-yellow-300"
                >
                  logout
                </button>
              </>
            ) : (
              <>
                <Link to="/apply" className={`${linkBase} text-neutral-400 hover:text-yellow-400`}>apply</Link>
                <Link
                  to="/login"
                  className="px-4 py-2 bg-yellow-400 text-black text-[12px] uppercase tracking-widest font-semibold rounded hover:bg-yellow-300"
                >
                  login
                </Link>
              </>
            )}
          </div>
          {/* mobile toggle */}
          <button
            className="md:hidden text-yellow-400 text-sm uppercase tracking-widest"
            onClick={() => setOpen((v) => !v)}
            aria-label="Toggle menu"
          >
            {open ? 'close' : 'menu'}
          </button>
        </div>

        {/* mobile menu */}
        {open && (
          <div className="md:hidden pb-4 space-y-1">
            {NAV.map((item) => (
              <div key={item.to}>
                <Link
                  to={item.to}
                  onClick={() => setOpen(false)}
                  className="block py-2 text-sm uppercase tracking-widest text-neutral-300 hover:text-yellow-400"
                >
                  {item.label}
                </Link>
                {item.children && (
                  <div className="pl-4 pb-1 space-y-1">
                    {item.children.map((c) => (
                      <Link
                        key={c.to}
                        to={c.to}
                        onClick={() => setOpen(false)}
                        className="block py-1 text-xs lowercase text-neutral-400 hover:text-yellow-400"
                      >
                        {c.label}
                      </Link>
                    ))}
                  </div>
                )}
              </div>
            ))}
            <div className="pt-3 flex gap-3">
              {user ? (
                <>
                  <Link to={DASHBOARD_FOR_ROLE[user.role] || '/'} onClick={() => setOpen(false)} className="px-4 py-2 border border-yellow-400 text-yellow-400 text-xs uppercase tracking-widest rounded">dashboard</Link>
                  <button onClick={() => { logout(); setOpen(false) }} className="px-4 py-2 bg-yellow-400 text-black text-xs uppercase tracking-widest font-semibold rounded">logout</button>
                </>
              ) : (
                <>
                  <Link to="/apply" onClick={() => setOpen(false)} className="px-4 py-2 border border-yellow-400 text-yellow-400 text-xs uppercase tracking-widest rounded">apply</Link>
                  <Link to="/login" onClick={() => setOpen(false)} className="px-4 py-2 bg-yellow-400 text-black text-xs uppercase tracking-widest font-semibold rounded">login</Link>
                </>
              )}
            </div>
          </div>
        )}
      </div>
    </header>
  )
}
