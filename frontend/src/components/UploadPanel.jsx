import React, { useState, useRef, useEffect } from 'react'
import { X, UploadCloud, FileText, CheckCircle, AlertCircle, Loader } from 'lucide-react'
import { uploadDocument, listDocuments } from '../api/chat'

const ACCEPTED = '.pdf,.docx,.doc,.txt,.md'
const ACCEPT_LABEL = 'PDF, DOCX, TXT, MD'

export default function UploadPanel({ onClose }) {
  const [documents, setDocuments] = useState([])
  const [uploading, setUploading] = useState(false)
  const [progress, setProgress] = useState(0)
  const [result, setResult] = useState(null) // { ok: bool, message: string }
  const [dragging, setDragging] = useState(false)
  const inputRef = useRef(null)

  useEffect(() => {
    listDocuments().then(setDocuments).catch(() => {})
  }, [])

  const handleFile = async (file) => {
    if (!file) return
    setResult(null)
    setUploading(true)
    setProgress(0)
    try {
      const data = await uploadDocument(file, setProgress)
      setResult({ ok: true, message: `"${data.filename}" ingested — ${data.chunks_ingested} chunks added to knowledge base.` })
      const docs = await listDocuments()
      setDocuments(docs)
    } catch (err) {
      const msg = err.response?.data?.detail || err.message || 'Upload failed'
      setResult({ ok: false, message: msg })
    } finally {
      setUploading(false)
      setProgress(0)
      if (inputRef.current) inputRef.current.value = ''
    }
  }

  const onInputChange = (e) => handleFile(e.target.files?.[0])

  const onDrop = (e) => {
    e.preventDefault()
    setDragging(false)
    handleFile(e.dataTransfer.files?.[0])
  }

  return (
    <div className="fixed inset-0 bg-black/40 z-50 flex justify-end" onClick={onClose}>
      <div
        className="w-full max-w-md bg-white h-full flex flex-col shadow-xl"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div className="flex items-center justify-between px-5 py-4 border-b border-gray-200 bg-bhashini-600">
          <div>
            <h2 className="text-white font-semibold text-base">Upload Documents</h2>
            <p className="text-bhashini-100 text-xs mt-0.5">Add to knowledge base instantly</p>
          </div>
          <button onClick={onClose} className="text-white/80 hover:text-white">
            <X className="w-5 h-5" />
          </button>
        </div>

        <div className="flex-1 overflow-y-auto p-5 space-y-5">
          {/* Drop zone */}
          <div
            onDragOver={(e) => { e.preventDefault(); setDragging(true) }}
            onDragLeave={() => setDragging(false)}
            onDrop={onDrop}
            onClick={() => !uploading && inputRef.current?.click()}
            className={`border-2 border-dashed rounded-xl p-8 text-center cursor-pointer transition-colors ${
              dragging
                ? 'border-bhashini-400 bg-bhashini-50'
                : 'border-gray-300 hover:border-bhashini-400 hover:bg-bhashini-50'
            } ${uploading ? 'pointer-events-none opacity-60' : ''}`}
          >
            <input
              ref={inputRef}
              type="file"
              accept={ACCEPTED}
              className="hidden"
              onChange={onInputChange}
              disabled={uploading}
            />
            {uploading ? (
              <div className="space-y-3">
                <Loader className="w-10 h-10 mx-auto text-bhashini-500 animate-spin" />
                <p className="text-sm text-gray-600">Processing… {progress}%</p>
                <div className="w-full bg-gray-200 rounded-full h-1.5">
                  <div
                    className="bg-bhashini-500 h-1.5 rounded-full transition-all"
                    style={{ width: `${progress}%` }}
                  />
                </div>
              </div>
            ) : (
              <>
                <UploadCloud className="w-10 h-10 mx-auto text-bhashini-400 mb-3" />
                <p className="text-sm font-medium text-gray-700">
                  Drag & drop or <span className="text-bhashini-600">browse</span>
                </p>
                <p className="text-xs text-gray-400 mt-1">{ACCEPT_LABEL} · max 10 MB</p>
              </>
            )}
          </div>

          {/* Result banner */}
          {result && (
            <div className={`flex items-start gap-3 p-3 rounded-xl text-sm ${
              result.ok
                ? 'bg-green-50 border border-green-200 text-green-800'
                : 'bg-red-50 border border-red-200 text-red-800'
            }`}>
              {result.ok
                ? <CheckCircle className="w-4 h-4 flex-shrink-0 mt-0.5" />
                : <AlertCircle className="w-4 h-4 flex-shrink-0 mt-0.5" />}
              <span>{result.message}</span>
            </div>
          )}

          {/* Uploaded documents list */}
          {documents.length > 0 && (
            <div>
              <p className="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-2">
                Uploaded documents ({documents.length})
              </p>
              <div className="space-y-2">
                {documents.map((doc) => (
                  <div
                    key={doc.filename}
                    className="flex items-center gap-3 bg-gray-50 border border-gray-200 rounded-lg px-3 py-2"
                  >
                    <FileText className="w-4 h-4 text-bhashini-500 flex-shrink-0" />
                    <span className="text-sm text-gray-700 flex-1 truncate">{doc.filename}</span>
                    <span className="text-xs text-gray-400">{doc.size_kb} KB</span>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
