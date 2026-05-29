import React from 'react'
import ReactMarkdown from 'react-markdown'
import { Ticket } from 'lucide-react'

export default function MessageBubble({ message }) {
  const isUser = message.role === 'user'

  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'} mb-4`}>
      {/* Bot avatar */}
      {!isUser && (
        <div className="w-8 h-8 rounded-full bg-bhashini-500 flex items-center justify-center text-white text-xs font-bold mr-2 flex-shrink-0 mt-1">
          BS
        </div>
      )}

      <div className={`max-w-[78%] ${isUser ? 'items-end' : 'items-start'} flex flex-col gap-1`}>
        {/* Bubble */}
        <div
          className={`px-4 py-3 rounded-2xl text-sm leading-relaxed ${
            isUser
              ? 'bg-bhashini-500 text-white rounded-br-md'
              : 'bg-white text-gray-800 shadow-sm border border-gray-100 rounded-bl-md'
          }`}
        >
          {isUser ? (
            <p>{message.content}</p>
          ) : (
            <ReactMarkdown
              components={{
                p: ({ children }) => <p className="mb-1 last:mb-0">{children}</p>,
                ol: ({ children }) => <ol className="list-decimal pl-4 space-y-0.5">{children}</ol>,
                ul: ({ children }) => <ul className="list-disc pl-4 space-y-0.5">{children}</ul>,
                li: ({ children }) => <li className="text-sm">{children}</li>,
                strong: ({ children }) => <strong className="font-semibold">{children}</strong>,
                code: ({ children }) => (
                  <code className="bg-gray-100 px-1 rounded text-xs">{children}</code>
                ),
              }}
            >
              {message.content}
            </ReactMarkdown>
          )}
        </div>

        {/* Ticket badge */}
        {message.ticketId && (
          <div className="flex items-center gap-1.5 bg-amber-50 border border-amber-200 text-amber-700 text-xs px-3 py-1.5 rounded-lg">
            <Ticket className="w-3 h-3" />
            <span>Ticket <span className="font-mono font-semibold">#{message.ticketId}</span> created</span>
          </div>
        )}

        {/* Sources */}
        {message.sources && message.sources.length > 0 && (
          <div className="flex flex-wrap gap-1">
            {message.sources.map((src, i) => (
              <span
                key={i}
                className="text-[11px] text-gray-400 bg-gray-100 px-2 py-0.5 rounded-full"
              >
                📄 {src}
              </span>
            ))}
          </div>
        )}

        {/* Timestamp */}
        <span className="text-[10px] text-gray-400">
          {message.timestamp}
        </span>
      </div>

      {/* User avatar */}
      {isUser && (
        <div className="w-8 h-8 rounded-full bg-gray-300 flex items-center justify-center text-gray-600 text-xs font-bold ml-2 flex-shrink-0 mt-1">
          U
        </div>
      )}
    </div>
  )
}
