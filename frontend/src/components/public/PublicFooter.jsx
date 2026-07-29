import React from 'react'
import { Link } from 'react-router-dom'

// Mirrors the projecteduaccess.com footer links + copyright line.
export default function PublicFooter() {
  return (
    <footer className="bg-black border-t border-yellow-400/30">
      <div className="max-w-6xl mx-auto px-4 py-10">
        <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-6">
          <div className="flex flex-wrap gap-6 text-[12px] uppercase tracking-widest text-neutral-400">
            <Link to="/" className="hover:text-yellow-400">home</Link>
            <Link to="/our-work" className="hover:text-yellow-400">explore our work</Link>
            <Link to="/team" className="hover:text-yellow-400">team</Link>
            <Link to="/faq" className="hover:text-yellow-400">faqs</Link>
            <Link to="/contact-us" className="hover:text-yellow-400">privacy policy</Link>
          </div>
          <p className="text-[12px] text-neutral-500">© {new Date().getFullYear()} by Project EduAccess.</p>
        </div>
      </div>
    </footer>
  )
}
