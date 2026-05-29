import React from 'react'
import { MessageSquare, Ticket, UploadCloud } from 'lucide-react'

const LANG_NAMES = {
  en: 'English', hi: 'Hindi', bn: 'Bengali', te: 'Telugu',
  mr: 'Marathi', ta: 'Tamil', gu: 'Gujarati', kn: 'Kannada',
  ml: 'Malayalam', pa: 'Punjabi', or: 'Odia', ur: 'Urdu', as: 'Assamese',
}

export default function Header({ detectedLang, onShowTickets, onShowUpload }) {
  return (
    <header className="bg-gradient-to-r from-bhashini-600 to-bhashini-700 shadow-md">
      <div className="max-w-4xl mx-auto px-4 py-3 flex items-center justify-between">
        {/* Brand */}
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 bg-white/20 rounded-xl flex items-center justify-center">
            <MessageSquare className="w-5 h-5 text-white" />
          </div>
          <div>
            <h1 className="text-white font-bold text-lg leading-tight">Bhashini Sahayak</h1>
            <p className="text-bhashini-100 text-xs">CAG Platform Assistant</p>
          </div>
        </div>

        {/* Right side */}
        <div className="flex items-center gap-3">
          {detectedLang && detectedLang !== 'en' && (
            <span className="bg-white/20 text-white text-xs px-3 py-1 rounded-full">
              🌐 {LANG_NAMES[detectedLang] ?? detectedLang}
            </span>
          )}
          <button
            onClick={onShowUpload}
            className="flex items-center gap-1.5 bg-white/20 hover:bg-white/30 text-white text-xs px-3 py-1.5 rounded-lg transition-colors"
          >
            <UploadCloud className="w-3.5 h-3.5" />
            Upload
          </button>
          <button
            onClick={onShowTickets}
            className="flex items-center gap-1.5 bg-white/20 hover:bg-white/30 text-white text-xs px-3 py-1.5 rounded-lg transition-colors"
          >
            <Ticket className="w-3.5 h-3.5" />
            Tickets
          </button>
        </div>
      </div>
    </header>
  )
}
