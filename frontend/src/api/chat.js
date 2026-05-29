import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || '',
  headers: { 'Content-Type': 'application/json' },
  timeout: 60000,
})

export async function sendMessage(query, sessionId) {
  const { data } = await api.post('/chat', { query, session_id: sessionId })
  return data
}

export async function fetchTickets() {
  const { data } = await api.get('/tickets')
  return data
}

export async function closeTicket(ticketId) {
  const { data } = await api.patch(`/tickets/${ticketId}/close`)
  return data
}

export async function checkHealth() {
  const { data } = await api.get('/health')
  return data
}

export async function uploadDocument(file, onProgress) {
  const form = new FormData()
  form.append('file', file)
  const { data } = await api.post('/upload', form, {
    headers: { 'Content-Type': 'multipart/form-data' },
    timeout: 300000, // 5 minutes — batch embedding can take a while
    onUploadProgress: (e) => onProgress && onProgress(Math.round((e.loaded * 100) / e.total)),
  })
  return data
}

export async function listDocuments() {
  const { data } = await api.get('/documents')
  return data.documents
}
