import React, { useEffect, useState } from 'react'
import api from '../../services/api'
import { Page, PageTitle, Prose } from '../../components/public/ui'

function Item({ faq }){
  const [open, setOpen] = useState(false)
  return (
    <div className="border border-yellow-400/30 rounded-md">
      <button
        onClick={() => setOpen((v) => !v)}
        className="w-full flex items-center justify-between text-left px-4 py-3 text-neutral-100 hover:text-yellow-400"
      >
        <span className="font-medium">{faq.question}</span>
        <span className="text-yellow-400 ml-4">{open ? '–' : '+'}</span>
      </button>
      {open && <p className="px-4 pb-4 text-neutral-300 leading-relaxed text-sm">{faq.answer}</p>}
    </div>
  )
}

export default function FAQ(){
  const [faqs, setFaqs] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    async function load(){
      try { setFaqs((await api.get('/api/public/faqs')).data) }
      catch { /* leave empty */ }
      finally { setLoading(false) }
    }
    load()
  }, [])

  // Group by category for a tidy layout.
  const groups = faqs.reduce((acc, f) => {
    const k = f.category || 'General'
    ;(acc[k] = acc[k] || []).push(f)
    return acc
  }, {})

  return (
    <Page>
      <PageTitle>frequently asked questions</PageTitle>
      <Prose className="mt-8 max-w-3xl">
        <p>
          Answers to the questions we hear most often. Can't find what you're looking for? Ask{' '}
          <span className="text-yellow-400">Noor</span> (bottom-right) or head to the Contact page.
        </p>
      </Prose>

      {loading ? (
        <p className="mt-8 text-neutral-400">Loading…</p>
      ) : faqs.length === 0 ? (
        <p className="mt-8 text-neutral-400">No FAQs published yet.</p>
      ) : (
        <div className="mt-10 space-y-10 max-w-3xl">
          {Object.entries(groups).map(([category, items]) => (
            <div key={category}>
              <h2 className="text-xs uppercase tracking-widest text-yellow-400 mb-3">{category}</h2>
              <div className="space-y-2">
                {items.map((f) => <Item key={f.id} faq={f} />)}
              </div>
            </div>
          ))}
        </div>
      )}
    </Page>
  )
}
