import React, { useEffect, useRef } from 'react'
import MessageBubble from './MessageBubble'

const WELCOME = {
  id: 'welcome',
  role: 'bot',
  content:
    'Namaste! I am **Bhashini Sahayak**, your CAG platform assistant. ' +
    'I can help you with:\n\n' +
    '- **Onboarding** — How to invite and register CEOs, Super Admins, Office Admins, and End Users\n' +
    '- **Document Translation** — Upload, translate, vet, format, and dispatch documents\n\n' +
    'You can ask me in **English or any Indian language** 🇮🇳',
  timestamp: '',
  sources: [],
}

export default function ChatWindow({ messages, isLoading }) {
  const bottomRef = useRef(null)

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, isLoading])

  return (
    <div className="flex-1 overflow-y-auto scrollbar-thin px-4 py-6 space-y-1">
      {/* Welcome */}
      <MessageBubble message={WELCOME} />

      {/* Conversation */}
      {messages.map((msg) => (
        <MessageBubble key={msg.id} message={msg} />
      ))}

      {/* Typing indicator */}
      {isLoading && (
        <div className="flex justify-start mb-4">
          <div className="w-8 h-8 rounded-full bg-bhashini-500 flex items-center justify-center text-white text-xs font-bold mr-2 flex-shrink-0 mt-1">
            BS
          </div>
          <div className="bg-white border border-gray-100 shadow-sm rounded-2xl rounded-bl-md px-4 py-3">
            <div className="flex gap-1 items-center h-5">
              <span className="w-2 h-2 bg-bhashini-400 rounded-full animate-bounce [animation-delay:-0.3s]" />
              <span className="w-2 h-2 bg-bhashini-400 rounded-full animate-bounce [animation-delay:-0.15s]" />
              <span className="w-2 h-2 bg-bhashini-400 rounded-full animate-bounce" />
            </div>
          </div>
        </div>
      )}

      <div ref={bottomRef} />
    </div>
  )
}
