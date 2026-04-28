import { useState, useCallback } from 'react'
import { useNavigate } from 'react-router-dom'
import { detectDisease } from '../services/api'

export default function Upload() {
  const [file, setFile] = useState<File | null>(null)
  const [preview, setPreview] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const navigate = useNavigate()

  const handleFile = (f: File) => {
    setFile(f)
    setPreview(URL.createObjectURL(f))
    setError(null)
  }

  const onDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault()
    const f = e.dataTransfer.files[0]
    if (f) handleFile(f)
  }, [])

  const onFileInput = (e: React.ChangeEvent<HTMLInputElement>) => {
    const f = e.target.files?.[0]
    if (f) handleFile(f)
  }

  const handleSubmit = async () => {
    if (!file) return
    setLoading(true)
    setError(null)
    try {
      const result = await detectDisease(file)
      navigate('/results', { state: { result } })
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Detection failed. Try again.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div>
      <h1 className="text-2xl font-bold text-green-800 mb-2">Crop Disease Detection</h1>
      <p className="text-gray-500 mb-6">Upload a leaf photo to get an instant diagnosis.</p>

      {/* Drop Zone */}
      <div
        onDrop={onDrop}
        onDragOver={(e) => e.preventDefault()}
        onClick={() => document.getElementById('file-input')?.click()}
        className="border-2 border-dashed border-green-400 rounded-xl p-10 text-center cursor-pointer hover:bg-green-50 transition"
      >
        {preview ? (
          <img src={preview} alt="preview" className="max-h-64 mx-auto rounded-lg object-contain" />
        ) : (
          <div>
            <p className="text-4xl mb-2">🌿</p>
            <p className="text-gray-500">Drag & drop a leaf image here</p>
            <p className="text-gray-400 text-sm mt-1">or click to browse</p>
          </div>
        )}
        <input id="file-input" type="file" accept="image/*" className="hidden" onChange={onFileInput} />
      </div>

      {file && (
        <p className="text-sm text-gray-500 mt-2 text-center">{file.name}</p>
      )}

      {error && (
        <div className="mt-4 bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
          {error}
        </div>
      )}

      <button
        onClick={handleSubmit}
        disabled={!file || loading}
        className="mt-6 w-full bg-green-700 text-white py-3 rounded-xl font-semibold text-lg hover:bg-green-800 disabled:opacity-40 disabled:cursor-not-allowed transition"
      >
        {loading ? 'Analyzing...' : 'Detect Disease'}
      </button>
    </div>
  )
}