import React, { useContext, useState } from 'react'
import { Outlet, Link, useLocation, useSearchParams } from 'react-router-dom'
import { AuthContext } from '../../context/AuthContext'
import { NAV } from '../../config/navConfig'

// Authenticated app shell: slim top bar + role-scoped left sidebar.
// The sidebar content is entirely driven by NAV[user.role], so admin, mentor,
// mentee and reviewer each get a visibly distinct app.
export default function AppLayout() {
  const { user, loading, logout } = useContext(AuthContext)
  const location = useLocation()
  const [searchParams] = useSearchParams()
  const [open, setOpen] = useState(false)

  if (loading) return null
  const cfg = user ? NAV[user.role] : null
  // Not authenticated (or unknown role): let the child ProtectedRoute redirect.
  if (!cfg) return <Outlet />

  // Resolve which nav item is active + the current page title.
  const isActive = (item) => {
    if (cfg.mode === 'tab') {
      const cur = searchParams.get('tab') || cfg.defaultTab
      return cur === item.tab
    }
    const cur = (location.hash || '').replace('#', '') || cfg.items[0].hash
    return cur === item.hash
  }
  const hrefFor = (item) =>
    cfg.mode === 'tab' ? `${cfg.base}?tab=${item.tab}` : `${cfg.base}#${item.hash}`
  const activeItem = cfg.items.find(isActive) || cfg.items[0]

  const SidebarLinks = (
    <nav className="space-y-1">
      {cfg.items.map((item) => (
        <Link
          key={item.label}
          to={hrefFor(item)}
          onClick={() => setOpen(false)}
          className={`block px-3 py-2 rounded-md text-sm transition ${
            isActive(item)
              ? 'bg-yellow-400 text-black font-medium'
              : 'text-neutral-300 hover:text-white hover:bg-white/5'
          }`}
        >
          {item.label}
        </Link>
      ))}
    </nav>
  )

  return (
    <div className="min-h-screen bg-neutral-50 text-neutral-900 flex">
      {/* Sidebar (desktop) */}
      <aside className="hidden md:flex md:flex-col w-60 shrink-0 bg-neutral-950 border-r border-black">
        <Link to="/" className="flex items-baseline gap-1.5 px-5 py-5 border-b border-white/10">
          <span className="text-lg font-extrabold text-white">edu</span>
          <span className="text-lg font-extrabold text-yellow-400">access</span>
        </Link>
        <div className="px-3 py-4">
          <p className="px-3 pb-2 text-[10px] uppercase tracking-widest text-neutral-500">{cfg.title}</p>
          {SidebarLinks}
        </div>
      </aside>

      {/* Main column */}
      <div className="flex-1 min-w-0 flex flex-col">
        {/* Top bar */}
        <header className="sticky top-0 z-30 bg-white border-b border-neutral-200">
          <div className="flex items-center justify-between px-4 md:px-8 h-14">
            <div className="flex items-center gap-3 min-w-0">
              <button
                className="md:hidden text-neutral-700 text-sm"
                onClick={() => setOpen((v) => !v)}
                aria-label="Toggle menu"
              >
                ☰
              </button>
              <span className="text-sm font-medium text-neutral-800 truncate">{activeItem?.label}</span>
            </div>
            <div className="flex items-center gap-3">
              <span className="hidden sm:flex items-center gap-2 text-sm text-neutral-600">
                {user.full_name}
                <span className="text-[10px] font-semibold uppercase tracking-wide px-2 py-0.5 rounded-full bg-yellow-100 text-yellow-800">
                  {user.role}
                </span>
              </span>
              <button
                onClick={logout}
                className="px-3 py-1.5 text-xs font-medium rounded-md border border-neutral-300 text-neutral-700 hover:bg-neutral-50"
              >
                Logout
              </button>
            </div>
          </div>
          {/* Mobile drawer */}
          {open && (
            <div className="md:hidden bg-neutral-950 px-3 py-4">
              <p className="px-3 pb-2 text-[10px] uppercase tracking-widest text-neutral-500">{cfg.title}</p>
              {SidebarLinks}
            </div>
          )}
        </header>

        <main className="flex-1 px-4 md:px-8 py-8">
          <div className="max-w-6xl mx-auto">
            <Outlet />
          </div>
        </main>
      </div>
    </div>
  )
}
