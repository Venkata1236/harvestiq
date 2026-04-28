import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { getDetections, deleteDetection } from '../services/api'

interface Detection {
  id: number
  display_name: string
  crop_type: string
  confidence: number
  severity: string
  image_filename: string
  created_at: string
}

const severityColor: Record<string, string> = {
  low:      'bg-green-100 text-green-800',
  medium:   'bg-yellow-100 text-yellow-800',
  high:     'bg-orange-100 text-orange-800',
  critical: 'bg-red-100 text-red-800',
}

export default function History() {
  const [detections, setDetections] = useState<Detection[]>([])
  const [loading, setLoading] = useState(true)
  const navigate = useNavigate()

  const fetchDetections = async () => {
    try {
      const data = await getDetections()
      setDetections(data.detections)
    } catch (err) {
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  const handleDelete = async (id: number) => {
    await deleteDetection(id)
    setDetections((prev) => prev.filter((d) => d.id !== id))
  }

  useEffect(() => {
    fetchDetections()
  }, [])

  if (loading) return <p className="text-center text-gray-400 py-20">Loading history...</p>

  if (detections.length === 0) {
    return (
      <div className="text-center py-20">
        <p className="text-4xl mb-3">🌱</p>
        <p className="text-gray-500">No detections yet.</p>
        <button onClick={() => navigate('/')} className="mt-4 bg-green-700 text-white px-6 py-2 rounded-lg">
          Make Your First Detection
        </button>
      </div>
    )
  }

  return (
    <div>
      <h1 className="text-2xl font-bold text-green-800 mb-6">Detection History</h1>
      <div className="space-y-4">
        {detections.map((d) => (
          <div key={d.id} className="bg-white rounded-xl shadow p-5 flex items-center justify-between">
            <div>
              <div className="flex items-center gap-2">
                <h3 className="font-semibold text-gray-800">{d.display_name}</h3>
                <span className={`px-2 py-0.5 rounded-full text-xs font-medium capitalize ${severityColor[d.severity] || 'bg-gray-100 text-gray-700'}`}>
                  {d.severity}
                </span>
              </div>
              <p className="text-sm text-gray-500 mt-1">
                {d.crop_type} · {d.confidence}% confidence
              </p>
              <p className="text-xs text-gray-400 mt-1">
                {new Date(d.created_at).toLocaleString()}
              </p>
            </div>
            <button
              onClick={() => handleDelete(d.id)}
              className="text-red-400 hover:text-red-600 text-xl transition"
              title="Delete"
            >
              🗑️
            </button>
          </div>
        ))}
      </div>
    </div>
  )
}