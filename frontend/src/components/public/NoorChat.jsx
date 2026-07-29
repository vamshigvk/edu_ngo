import React, { useEffect, useRef, useState } from 'react'
import api from '../../services/api'

// Replica of the "Noor" (Wix AI Assistant) widget on projecteduaccess.com —
// a floating launcher + right-docked panel. Answers are FAQ-grounded via
// POST /api/public/chat (static now; an SLM can slot in behind that endpoint).

const GREETING = [
  "Hi, I'm Noor 👋",
  'Before we start, please note that I am powered by AI technology and can make mistakes. I advise verifying the accuracy of results before relying on them.',
  'With that, how can I help you today?',
]

const SUGGESTIONS = [
  'I want to study abroad',
  'Tell me about the Graduate Mentorship Programme',
  'Tell me about your Fellowships',
  'Workshops & resources',
  'Tell me about Guides on Application Documents',
]

function Badge() {
  return (
    <span className="inline-flex items-center justify-center h-6 w-6 rounded bg-black text-yellow-400 text-[10px] font-bold">
      AI
    </span>
  )
}

export default function NoorChat() {
  const [open, setOpen] = useState(false)
  const [messages, setMessages] = useState([]) // {from:'bot'|'user', text}
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const scrollRef = useRef(null)

  const started = messages.some((m) => m.from === 'user')

  useEffect(() => {
    if (open && messages.length === 0) {
      setMessages(GREETING.map((text) => ({ from: 'bot', text })))
    }
  }, [open, messages.length])

  useEffect(() => {
    if (scrollRef.current) scrollRef.current.scrollTop = scrollRef.current.scrollHeight
  }, [messages, loading, open])

  async function ask(text) {
    const q = (text || '').trim()
    if (!q || loading) return
    setInput('')
    setMessages((m) => [...m, { from: 'user', text: q }])
    setLoading(true)
    try {
      const { data } = await api.post('/api/public/chat', { message: q })
      setMessages((m) => [...m, { from: 'bot', text: data.answer }])
    } catch {
      setMessages((m) => [...m, { from: 'bot', text: 'Sorry, I could not reach the server just now. Please try again.' }])
    } finally {
      setLoading(false)
    }
  }

  // Launcher (closed state)
  if (!open) {
    return (
      <button
        onClick={() => setOpen(true)}
        className="fixed bottom-5 right-5 z-50 flex items-center gap-2 pl-2 pr-4 py-2 rounded-full bg-white text-neutral-800 shadow-lg ring-1 ring-yellow-400/70 hover:ring-yellow-400 hover:shadow-xl transition"
        aria-label="Chat with Noor"
      >
        <Badge />
        <span className="text-sm font-medium">Chat with Noor</span>
      </button>
    )
  }

  // Panel (open state)
  return (
    <div className="fixed bottom-5 right-5 z-50 w-[92vw] max-w-sm h-[32rem] max-h-[80vh] flex flex-col rounded-xl overflow-hidden shadow-2xl border border-neutral-200 bg-white">
      {/* Header */}
      <div className="flex items-center justify-between px-4 py-3 bg-yellow-400 text-black">
        <div className="flex items-center gap-2">
          <Badge />
          <span className="text-sm font-semibold">Chat with Noor by EduAccess</span>
        </div>
        <button onClick={() => setOpen(false)} aria-label="Minimize" className="text-black/70 hover:text-black text-lg leading-none">—</button>
      </div>

      {/* Messages */}
      <div ref={scrollRef} className="flex-1 overflow-y-auto px-3 py-4 space-y-3 bg-neutral-50">
        {messages.map((m, i) => (
          <div key={i} className={`flex ${m.from === 'user' ? 'justify-end' : 'justify-start'}`}>
            <div
              className={`max-w-[85%] rounded-2xl px-3 py-2 text-sm leading-relaxed ${
                m.from === 'user'
                  ? 'bg-yellow-400 text-black rounded-br-sm'
                  : 'bg-white border border-neutral-200 text-neutral-800 rounded-bl-sm'
              }`}
            >
              {m.text}
            </div>
          </div>
        ))}

        {/* Suggested prompts (only before the first user message) */}
        {!started && (
          <div className="space-y-2 pt-1">
            {SUGGESTIONS.map((s) => (
              <button
                key={s}
                onClick={() => ask(s)}
                className="block w-full text-left text-sm px-3 py-2 rounded-lg border border-neutral-200 bg-white text-neutral-700 hover:border-yellow-400 hover:bg-yellow-50 transition"
              >
                {s}
              </button>
            ))}
          </div>
        )}

        {loading && (
          <div className="flex justify-start">
            <div className="bg-white border border-neutral-200 text-neutral-400 text-sm rounded-2xl rounded-bl-sm px-3 py-2">Noor is typing…</div>
          </div>
        )}
      </div>

      {/* Input */}
      <form
        onSubmit={(e) => { e.preventDefault(); ask(input) }}
        className="flex items-center gap-2 border-t border-neutral-200 px-3 py-2 bg-white"
      >
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type your message…"
          className="flex-1 text-sm outline-none px-2 py-2 text-neutral-800 placeholder-neutral-400"
        />
        <button
          type="submit"
          disabled={loading || !input.trim()}
          className="h-8 w-8 flex items-center justify-center rounded-full bg-yellow-400 text-black disabled:opacity-40"
          aria-label="Send"
        >
          ➤
        </button>
      </form>
    </div>
  )
}
