import React, { useState, useRef } from 'react'
import { Send } from 'lucide-react'

export default function InputBar({ onSend, isLoading }) {
  const [text, setText] = useState('')
  const textareaRef = useRef(null)

  const handleSubmit = () => {
    const trimmed = text.trim()
    if (!trimmed || isLoading) return
    onSend(trimmed)
    setText('')
    textareaRef.current?.focus()
  }

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSubmit()
    }
  }

  return (
    <div className="border-t border-gray-200 bg-white px-4 py-3">
      <div className="max-w-4xl mx-auto flex items-end gap-3">
        <div className="flex-1 relative">
          <textarea
            ref={textareaRef}
            value={text}
            onChange={(e) => setText(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Ask about onboarding, document translation, roles… (any Indian language)"
            rows={1}
            disabled={isLoading}
            className="w-full resize-none rounded-xl border border-gray-300 focus:border-bhashini-500 focus:ring-2 focus:ring-bhashini-200 outline-none px-4 py-3 text-sm text-gray-800 placeholder-gray-400 max-h-32 overflow-y-auto transition disabled:opacity-60"
            style={{ lineHeight: '1.5' }}
            onInput={(e) => {
              e.target.style.height = 'auto'
              e.target.style.height = `${Math.min(e.target.scrollHeight, 128)}px`
            }}
          />
        </div>
        <button
          onClick={handleSubmit}
          disabled={!text.trim() || isLoading}
          className="w-11 h-11 rounded-xl bg-bhashini-500 hover:bg-bhashini-600 disabled:bg-gray-300 text-white flex items-center justify-center transition-colors flex-shrink-0"
          aria-label="Send message"
        >
          <Send className="w-4 h-4" />
        </button>
      </div>
      <p className="max-w-4xl mx-auto text-[10px] text-gray-400 mt-1.5 px-1">
        Press Enter to send · Shift+Enter for new line
      </p>
    </div>
  )
}
