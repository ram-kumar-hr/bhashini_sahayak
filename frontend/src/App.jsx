import { useState, useCallback } from 'react'
import Header from './components/Header'
import ChatWindow from './components/ChatWindow'
import InputBar from './components/InputBar'
import TicketsPanel from './components/TicketsPanel'
import UploadPanel from './components/UploadPanel'
import { sendMessage } from './api/chat'

let msgCounter = 0
const newId = () => `msg-${++msgCounter}`
const fmt = () => new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })

export default function App() {
  const [messages, setMessages] = useState([])
  const [isLoading, setIsLoading] = useState(false)
  const [sessionId] = useState(() => crypto.randomUUID())
  const [detectedLang, setDetectedLang] = useState(null)
  const [showTickets, setShowTickets] = useState(false)
  const [showUpload, setShowUpload] = useState(false)

  const handleSend = useCallback(async (query) => {
    setMessages((prev) => [
      ...prev,
      { id: newId(), role: 'user', content: query, timestamp: fmt() },
    ])
    setIsLoading(true)

    try {
      const data = await sendMessage(query, sessionId)
      setDetectedLang(data.detected_language)
      setMessages((prev) => [
        ...prev,
        {
          id: newId(),
          role: 'bot',
          content: data.response,
          timestamp: fmt(),
          ticketId: data.ticket_id ?? null,
          sources: data.sources ?? [],
        },
      ])
    } catch {
      setMessages((prev) => [
        ...prev,
        {
          id: newId(),
          role: 'bot',
          content: '⚠️ Unable to reach the server. Please make sure the backend is running on port 8000.',
          timestamp: fmt(),
          sources: [],
        },
      ])
    } finally {
      setIsLoading(false)
    }
  }, [sessionId])

  return (
    <div className="flex flex-col h-screen bg-gray-50">
      <Header
        detectedLang={detectedLang}
        onShowUpload={() => setShowUpload(true)}
        onShowTickets={() => setShowTickets(true)}
      />

      <main className="flex-1 overflow-hidden flex flex-col max-w-4xl w-full mx-auto">
        <ChatWindow messages={messages} isLoading={isLoading} />
        <InputBar onSend={handleSend} isLoading={isLoading} />
      </main>

      {showUpload && <UploadPanel onClose={() => setShowUpload(false)} />}
      {showTickets && <TicketsPanel onClose={() => setShowTickets(false)} />}
    </div>
  )
}
