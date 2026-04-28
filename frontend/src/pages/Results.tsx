import { useLocation, useNavigate } from 'react-router-dom'

const severityColor: Record<string, string> = {
  low:      'bg-green-100 text-green-800',
  medium:   'bg-yellow-100 text-yellow-800',
  high:     'bg-orange-100 text-orange-800',
  critical: 'bg-red-100 text-red-800',
}

export default function Results() {
  const { state } = useLocation()
  const navigate = useNavigate()
  const r = state?.result

  if (!r) {
    return (
      <div className="text-center py-20">
        <p className="text-gray-500">No result found.</p>
        <button onClick={() => navigate('/')} className="mt-4 text-green-700 underline">
          Go back
        </button>
      </div>
    )
  }

  if (r.status === 'low_confidence') {
    return (
      <div className="bg-yellow-50 border border-yellow-200 rounded-xl p-6 text-center">
        <p className="text-2xl mb-2">⚠️</p>
        <h2 className="text-lg font-semibold text-yellow-800">{r.message}</h2>
        <button onClick={() => navigate('/')} className="mt-4 bg-green-700 text-white px-6 py-2 rounded-lg">
          Try Again
        </button>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-white rounded-xl shadow p-6">
        <div className="flex items-start justify-between">
          <div>
            <h2 className="text-2xl font-bold text-gray-800">{r.display_name}</h2>
            <p className="text-gray-500 mt-1">Crop: <span className="font-medium capitalize">{r.crop_type}</span></p>
          </div>
          <span className={`px-3 py-1 rounded-full text-sm font-semibold capitalize ${severityColor[r.severity] || 'bg-gray-100 text-gray-700'}`}>
            {r.severity}
          </span>
        </div>
        <div className="mt-4 flex items-center gap-3">
          <span className="text-gray-500 text-sm">Confidence</span>
          <div className="flex-1 bg-gray-200 rounded-full h-2">
            <div className="bg-green-600 h-2 rounded-full" style={{ width: `${r.confidence}%` }} />
          </div>
          <span className="text-sm font-semibold text-green-700">{r.confidence}%</span>
        </div>
      </div>

      {/* Symptoms & Causes */}
      <div className="grid grid-cols-2 gap-4">
        <div className="bg-white rounded-xl shadow p-5">
          <h3 className="font-semibold text-gray-700 mb-2">🔍 Symptoms</h3>
          <p className="text-gray-600 text-sm">{r.symptoms}</p>
        </div>
        <div className="bg-white rounded-xl shadow p-5">
          <h3 className="font-semibold text-gray-700 mb-2">🧫 Causes</h3>
          <p className="text-gray-600 text-sm">{r.causes}</p>
        </div>
      </div>

      {/* AI Diagnosis */}
      <div className="bg-white rounded-xl shadow p-5">
        <h3 className="font-semibold text-gray-700 mb-2">🤖 AI Diagnosis</h3>
        <p className="text-gray-600 text-sm whitespace-pre-line">{r.diagnosis_report}</p>
      </div>

      {/* Treatment Plan */}
      <div className="bg-green-50 rounded-xl shadow p-5 border border-green-200">
        <h3 className="font-semibold text-green-800 mb-2">💊 Treatment Plan</h3>
        <p className="text-green-900 text-sm whitespace-pre-line">{r.treatment_plan}</p>
      </div>

      {/* Actions */}
      <div className="flex gap-3">
        <button onClick={() => navigate('/')} className="flex-1 bg-green-700 text-white py-3 rounded-xl font-semibold hover:bg-green-800 transition">
          New Detection
        </button>
        <button onClick={() => navigate('/history')} className="flex-1 bg-white border border-green-700 text-green-700 py-3 rounded-xl font-semibold hover:bg-green-50 transition">
          View History
        </button>
      </div>
    </div>
  )
}