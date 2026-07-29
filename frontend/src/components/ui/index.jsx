import React from 'react'

// --- Sleek, lightweight primitives for the authenticated app (light theme) ---
// White cards, thin borders, small radii, restrained shadows; black + yellow accents.

export function Card({ children, className = '', as: Tag = 'div', ...rest }) {
  return (
    <Tag className={`bg-white border border-neutral-200 rounded-lg shadow-sm ${className}`} {...rest}>
      {children}
    </Tag>
  )
}

// Card with a titled header row.
export function Panel({ title, actions, children, className = '' }) {
  return (
    <Card className={className}>
      {(title || actions) && (
        <div className="flex items-center justify-between gap-3 px-5 py-3.5 border-b border-neutral-100">
          {title && <h3 className="text-sm font-semibold text-neutral-800">{title}</h3>}
          {actions}
        </div>
      )}
      <div className="p-5">{children}</div>
    </Card>
  )
}

export function PageHeader({ title, subtitle, actions }) {
  return (
    <div className="flex flex-wrap items-end justify-between gap-4 mb-6">
      <div>
        <h1 className="text-2xl font-semibold text-neutral-900">{title}</h1>
        {subtitle && <p className="mt-1 text-sm text-neutral-500">{subtitle}</p>}
      </div>
      {actions && <div className="flex items-center gap-2">{actions}</div>}
    </div>
  )
}

const BTN = {
  primary: 'bg-neutral-900 text-white hover:bg-neutral-800',
  accent: 'bg-yellow-400 text-black hover:bg-yellow-300',
  ghost: 'border border-neutral-300 text-neutral-700 hover:bg-neutral-50',
  danger: 'bg-red-600 text-white hover:bg-red-500',
}
export function Button({ variant = 'primary', size = 'md', className = '', children, ...rest }) {
  const sz = size === 'sm' ? 'px-3 py-1.5 text-xs' : 'px-4 py-2 text-sm'
  return (
    <button
      className={`inline-flex items-center justify-center rounded-md font-medium transition disabled:opacity-50 disabled:cursor-not-allowed ${sz} ${BTN[variant]} ${className}`}
      {...rest}
    >
      {children}
    </button>
  )
}

const BADGE = {
  gray: 'bg-neutral-100 text-neutral-600',
  green: 'bg-green-100 text-green-700',
  yellow: 'bg-yellow-100 text-yellow-800',
  orange: 'bg-orange-100 text-orange-700',
  red: 'bg-red-100 text-red-700',
}
export function Badge({ tone = 'gray', children, className = '' }) {
  return (
    <span className={`inline-block text-[10px] font-medium uppercase tracking-wide px-2 py-0.5 rounded-full ${BADGE[tone]} ${className}`}>
      {children}
    </span>
  )
}

export function Stat({ label, value }) {
  return (
    <Card className="p-4">
      <p className="text-xs uppercase tracking-wide text-neutral-500">{label}</p>
      <p className="mt-1 text-2xl font-bold text-neutral-900">{value}</p>
    </Card>
  )
}

export function EmptyState({ children }) {
  return <p className="text-sm text-neutral-500 py-6 text-center">{children}</p>
}

export function ErrorBanner({ children }) {
  if (!children) return null
  return <div className="mb-6 p-3 bg-red-50 border border-red-200 text-red-700 rounded-md text-sm">{children}</div>
}

// Lightweight declarative table. columns: [{ key, label, render?(row), className? }]
export function DataTable({ columns, rows, empty = 'Nothing here yet.', rowKey = (r, i) => r.id ?? i }) {
  return (
    <div className="overflow-x-auto border border-neutral-200 rounded-lg">
      <table className="min-w-full text-sm">
        <thead className="bg-neutral-50 text-neutral-500">
          <tr className="text-left">
            {columns.map((c) => (
              <th key={c.key} className={`py-2.5 px-4 font-medium text-xs uppercase tracking-wide ${c.className || ''}`}>
                {c.label}
              </th>
            ))}
          </tr>
        </thead>
        <tbody className="divide-y divide-neutral-100">
          {rows.length === 0 ? (
            <tr><td colSpan={columns.length} className="py-6 px-4 text-center text-neutral-400">{empty}</td></tr>
          ) : (
            rows.map((row, i) => (
              <tr key={rowKey(row, i)} className="hover:bg-yellow-50/40 align-top">
                {columns.map((c) => (
                  <td key={c.key} className={`py-2.5 px-4 text-neutral-700 ${c.className || ''}`}>
                    {c.render ? c.render(row) : row[c.key]}
                  </td>
                ))}
              </tr>
            ))
          )}
        </tbody>
      </table>
    </div>
  )
}

// Text/select/textarea inputs sharing one clean style.
export const inputClass =
  'w-full rounded-md border border-neutral-300 px-3 py-2 text-sm text-neutral-800 outline-none focus:border-yellow-500 focus:ring-1 focus:ring-yellow-400'
