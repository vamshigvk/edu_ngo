import React from 'react'
import { Link } from 'react-router-dom'

// --- Shared public-site building blocks (mirrors projecteduaccess.com styling) ---
// Dark canvas, yellow accents, lowercase serif titles flanked by thin rules.

// Big lowercase page title with a leading yellow rule, e.g. "— about us".
export function PageTitle({ children, className = '' }) {
  return (
    <div className={`flex items-center gap-4 ${className}`}>
      <span className="h-px w-10 bg-yellow-400 shrink-0" />
      <h1 className="font-serif text-4xl md:text-5xl font-light lowercase text-yellow-400">{children}</h1>
    </div>
  )
}

// Centered hero title flanked by rules on both sides (used on Home).
export function HeroRuleTitle({ children }) {
  return (
    <div className="flex items-center justify-center gap-5">
      <span className="hidden sm:block h-px w-16 md:w-28 bg-yellow-400" />
      <h1 className="font-serif text-3xl md:text-5xl font-light text-yellow-400 text-center">{children}</h1>
      <span className="hidden sm:block h-px w-16 md:w-28 bg-yellow-400" />
    </div>
  )
}

// Section heading (lowercase, smaller than the page title).
export function SectionTitle({ children, className = '' }) {
  return (
    <h2 className={`font-serif text-2xl md:text-3xl font-light lowercase text-yellow-400 ${className}`}>
      {children}
    </h2>
  )
}

// Readable body copy on the dark canvas.
export function Prose({ children, className = '' }) {
  return <div className={`space-y-4 text-neutral-300 leading-relaxed ${className}`}>{children}</div>
}

// A page wrapper providing consistent width + vertical rhythm.
export function Page({ children, className = '' }) {
  return <div className={`max-w-6xl mx-auto px-4 py-16 ${className}`}>{children}</div>
}

// Yellow-bordered card that links somewhere (the four Home tiles, resource lists).
export function LinkCard({ to, href, title, children }) {
  const inner = (
    <div className="group h-full border border-yellow-400/60 hover:border-yellow-400 hover:bg-yellow-400/5 transition rounded-md p-6 flex flex-col">
      <h3 className="font-serif text-xl lowercase text-yellow-400">{title}</h3>
      {children && <p className="mt-3 text-sm text-neutral-300 leading-relaxed flex-1">{children}</p>}
      <span className="mt-4 text-xs uppercase tracking-widest text-yellow-400/80 group-hover:text-yellow-300">
        learn more →
      </span>
    </div>
  )
  if (href) return <a href={href} target="_blank" rel="noreferrer">{inner}</a>
  return <Link to={to || '#'}>{inner}</Link>
}

// Primary (solid yellow) and ghost buttons.
export function Button({ to, href, children, variant = 'solid', onClick, type }) {
  const base = 'inline-block px-7 py-3 rounded font-semibold text-sm tracking-wide transition'
  const styles =
    variant === 'solid'
      ? 'bg-yellow-400 text-black hover:bg-yellow-300'
      : 'border border-yellow-400 text-yellow-400 hover:bg-yellow-400 hover:text-black'
  const cls = `${base} ${styles}`
  if (href) return <a href={href} target="_blank" rel="noreferrer" className={cls}>{children}</a>
  if (to) return <Link to={to} className={cls}>{children}</Link>
  return <button type={type || 'button'} onClick={onClick} className={cls}>{children}</button>
}

// A single impact statistic (used in the stats band).
export function Stat({ value, label }) {
  return (
    <div className="text-center">
      <div className="text-3xl md:text-4xl font-bold text-black">{value}</div>
      <div className="mt-1 text-[11px] md:text-xs uppercase tracking-widest text-black/70">{label}</div>
    </div>
  )
}
