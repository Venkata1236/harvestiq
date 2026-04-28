import { useLocation, useNavigate } from 'react-router-dom'

const severityConfig: Record<string, { bg: string; text: string; border: string; label: string }> = {
  low:      { bg: 'bg-green-50',  text: 'text-green-700',  border: 'border-green-300', label: 'Low' },
  moderate: { bg: 'bg-yellow-50', text: 'text-yellow-700', border: 'border-yellow-300', label: 'Moderate' },
  medium:   { bg: 'bg-yellow-50', text: 'text-yellow-700', border: 'border-yellow-300', label: 'Medium' },
  high:     { bg: 'bg-orange-50', text: 'text-orange-700', border: 'border-orange-300', label: 'High' },
  critical: { bg: 'bg-red-50',    text: 'text-red-700',    border: 'border-red-300',    label: 'Critical' },
}

const confidenceBarColor = (conf: number) => {
  if (conf >= 85) return 'bg-green-500'
  if (conf >= 65) return 'bg-yellow-500'
  return 'bg-orange-500'
}

function FormattedContent({
  raw,
  textColor = 'text-gray-700',
  bulletColor = 'text-green-600',
}: {
  raw: string
  textColor?: string
  bulletColor?: string
}) {
  if (!raw) return null

  const cleaned = raw
    .replace(/\*\*(.*?)\*\*/g, '$1')
    .replace(/##\s*/g, '')
    .trim()

  const normalised = cleaned.replace(/^\*\s+/gm, '• ')
  const parts = normalised.split(/(?=•\s)/)

  const paragraphs: string[] = []
  const bullets: string[] = []

  parts.forEach((part) => {
    const trimmed = part.trim()
    if (!trimmed) return
    if (trimmed.startsWith('•')) {
      const subBullets = trimmed.split(/\s*•\s+/).filter(Boolean)
      subBullets.forEach((b) => bullets.push(b.trim()))
    } else {
      const inline = trimmed.split(/\s*•\s+/)
      if (inline.length > 1) {
        paragraphs.push(inline[0].trim())
        inline.slice(1).forEach((b) => bullets.push(b.trim()))
      } else {
        paragraphs.push(trimmed)
      }
    }
  })

  return (
    <div className="space-y-3">
      {paragraphs.map((p, i) => {
        const isHeader = p.length < 50 && !p.endsWith('.') && /^[A-Z]/.test(p)
        return isHeader ? (
          <p key={i} className={`text-sm font-semibold ${textColor} mt-2`}>{p}</p>
        ) : (
          <p key={i} className={`text-sm leading-relaxed ${textColor}`}>{p}</p>
        )
      })}

      {bullets.length > 0 && (
        <ul className="space-y-2 mt-1">
          {bullets.map((b, i) => (
            <li key={i} className="flex items-start gap-2">
              <span className={`mt-0.5 font-bold text-base leading-none ${bulletColor}`}>•</span>
              <span className={`text-sm leading-relaxed ${textColor}`}>{b}</span>
            </li>
          ))}
        </ul>
      )}
    </div>
  )
}

export default function Results() {
  const { state } = useLocation()
  const navigate = useNavigate()
  const r = state?.result

  if (!r) {
    return (
      <div className="text-center py-20">
        <p className="text-gray-500">No result found.</p>
        <button
          onClick={() => navigate('/')}
          className="mt-4 text-green-700 underline"
        >
          Go back
        </button>
      </div>
    )
  }

  if (r.status === 'low_confidence') {
    return (
      <div className="max-w-lg mx-auto mt-10 bg-yellow-50 border border-yellow-200 rounded-2xl p-8 text-center shadow">
        <h2 className="text-lg font-semibold text-yellow-800">{r.message}</h2>
        <button
          onClick={() => navigate('/')}
          className="mt-5 bg-green-700 text-white px-8 py-2.5 rounded-xl font-semibold hover:bg-green-800 transition"
        >
          Try Again
        </button>
      </div>
    )
  }

  const sev = severityConfig[r.severity?.toLowerCase()] ?? {
    bg: 'bg-gray-50', text: 'text-gray-700', border: 'border-gray-200', label: r.severity,
  }

  return (
    <div className="max-w-3xl mx-auto space-y-5 py-6 px-4">

      {/* 1. Header card */}
      <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-6">
        <div className="flex items-start justify-between gap-4 flex-wrap">
          <div>
            <h2 className="text-2xl font-bold text-gray-900 leading-tight">{r.display_name}</h2>
            <p className="text-gray-500 mt-1 text-sm">
              Crop: <span className="font-medium text-gray-700 capitalize">{r.crop_type}</span>
            </p>
          </div>
          <span className={`shrink-0 px-4 py-1.5 rounded-full text-xs font-bold uppercase tracking-widest border ${sev.bg} ${sev.text} ${sev.border}`}>
            {sev.label}
          </span>
        </div>

        <div className="mt-5">
          <div className="flex justify-between mb-1.5">
            <span className="text-xs font-medium text-gray-500 uppercase tracking-wide">Confidence</span>
            <span className="text-sm font-bold text-gray-800">{r.confidence}%</span>
          </div>
          <div className="w-full bg-gray-100 rounded-full h-2.5 overflow-hidden">
            <div
              className={`h-2.5 rounded-full transition-all duration-700 ${confidenceBarColor(r.confidence)}`}
              style={{ width: `${r.confidence}%` }}
            />
          </div>
        </div>
      </div>

      {/* 2. Symptoms & Causes */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-5">
          <h3 className="font-semibold text-gray-800 text-sm uppercase tracking-wide mb-3">Symptoms</h3>
          <FormattedContent raw={r.symptoms} />
        </div>
        <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-5">
          <h3 className="font-semibold text-gray-800 text-sm uppercase tracking-wide mb-3">Causes</h3>
          <FormattedContent raw={r.causes} />
        </div>
      </div>

      {/* 3. AI Diagnosis */}
      <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-5">
        <h3 className="font-semibold text-gray-800 text-sm uppercase tracking-wide mb-4">AI Diagnosis</h3>
        <FormattedContent raw={r.diagnosis_report} />
      </div>

      {/* 4. GradCAM Heatmap */}
      {r.heatmap_base64 && (
        <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-5">
          <h3 className="font-semibold text-gray-800 text-sm uppercase tracking-wide mb-1">Disease Heatmap</h3>
          <p className="text-xs text-gray-400 mb-3">Red areas indicate where the AI detected disease</p>
          <img
            src={`data:image/png;base64,${r.heatmap_base64}`}
            alt="GradCAM heatmap"
            className="w-full rounded-lg border border-gray-200"
          />
        </div>
      )}

      {/* 5. Treatment Plan */}
      <div className="bg-green-50 rounded-2xl shadow-sm border border-green-200 p-5">
        <h3 className="font-semibold text-green-800 text-sm uppercase tracking-wide mb-4">Treatment Plan</h3>
        <FormattedContent
          raw={r.treatment_plan}
          textColor="text-green-900"
          bulletColor="text-green-600"
        />
      </div>

      {/* 6. Action buttons */}
      <div className="flex gap-3 pt-1">
        <button
          onClick={() => navigate('/')}
          className="flex-1 bg-green-700 text-white py-3 rounded-xl font-semibold hover:bg-green-800 active:scale-95 transition-all"
        >
          New Detection
        </button>
        <button
          onClick={() => navigate('/history')}
          className="flex-1 bg-white border-2 border-green-700 text-green-700 py-3 rounded-xl font-semibold hover:bg-green-50 active:scale-95 transition-all"
        >
          View History
        </button>
      </div>

    </div>
  )
}