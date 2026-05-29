import React, { useEffect, useState } from 'react'
import { X, RefreshCw, CheckCircle, Clock } from 'lucide-react'
import { fetchTickets, closeTicket } from '../api/chat'

const STATUS_STYLES = {
  open: 'bg-amber-100 text-amber-700',
  closed: 'bg-green-100 text-green-700',
}

const LANG_NAMES = {
  en: 'EN', hi: 'HI', bn: 'BN', te: 'TE', mr: 'MR',
  ta: 'TA', gu: 'GU', kn: 'KN', ml: 'ML', pa: 'PA',
  or: 'OR', ur: 'UR', as: 'AS',
}

export default function TicketsPanel({ onClose }) {
  const [tickets, setTickets] = useState([])
  const [loading, setLoading] = useState(true)
  const [closing, setClosing] = useState(null)

  const load = async () => {
    setLoading(true)
    try {
      const data = await fetchTickets()
      setTickets(data)
    } catch {
      // ignore
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => { load() }, [])

  const handleClose = async (id) => {
    setClosing(id)
    try {
      await closeTicket(id)
      await load()
    } finally {
      setClosing(null)
    }
  }

  return (
    <div className="fixed inset-0 bg-black/40 z-50 flex justify-end" onClick={onClose}>
      <div
        className="w-full max-w-md bg-white h-full flex flex-col shadow-xl"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div className="flex items-center justify-between px-5 py-4 border-b border-gray-200 bg-bhashini-600">
          <h2 className="text-white font-semibold text-base">Support Tickets</h2>
          <div className="flex items-center gap-2">
            <button
              onClick={load}
              className="text-white/80 hover:text-white"
              title="Refresh"
            >
              <RefreshCw className="w-4 h-4" />
            </button>
            <button onClick={onClose} className="text-white/80 hover:text-white">
              <X className="w-5 h-5" />
            </button>
          </div>
        </div>

        {/* Body */}
        <div className="flex-1 overflow-y-auto scrollbar-thin p-4 space-y-3">
          {loading ? (
            <div className="flex justify-center py-12">
              <div className="w-6 h-6 border-2 border-bhashini-400 border-t-transparent rounded-full animate-spin" />
            </div>
          ) : tickets.length === 0 ? (
            <div className="text-center py-12 text-gray-400">
              <CheckCircle className="w-10 h-10 mx-auto mb-3 text-gray-300" />
              <p className="text-sm">No tickets yet</p>
            </div>
          ) : (
            tickets.map((t) => (
              <div
                key={t.id}
                className="bg-gray-50 border border-gray-200 rounded-xl p-4 space-y-2"
              >
                <div className="flex items-start justify-between gap-2">
                  <span className="font-mono text-xs font-bold text-bhashini-600">
                    #{t.id}
                  </span>
                  <div className="flex items-center gap-1.5">
                    <span className="text-[10px] text-gray-400 bg-gray-200 px-1.5 py-0.5 rounded font-mono">
                      {LANG_NAMES[t.language] ?? t.language}
                    </span>
                    <span
                      className={`text-[10px] px-2 py-0.5 rounded-full font-medium ${
                        STATUS_STYLES[t.status] ?? 'bg-gray-100 text-gray-600'
                      }`}
                    >
                      {t.status}
                    </span>
                  </div>
                </div>

                <p className="text-sm text-gray-700 line-clamp-3">{t.query}</p>

                <div className="flex items-center justify-between">
                  <span className="flex items-center gap-1 text-[10px] text-gray-400">
                    <Clock className="w-3 h-3" />
                    {new Date(t.created_at).toLocaleString()}
                  </span>
                  {t.status === 'open' && (
                    <button
                      onClick={() => handleClose(t.id)}
                      disabled={closing === t.id}
                      className="text-xs text-green-600 hover:text-green-700 font-medium disabled:opacity-50"
                    >
                      {closing === t.id ? 'Closing…' : 'Mark Closed'}
                    </button>
                  )}
                </div>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  )
}
