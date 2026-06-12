import { AlertTriangle, CheckCircle2, Zap } from 'lucide-react'

export default function SkillGapCard({ skillGaps }) {
  if (!skillGaps || skillGaps.length === 0) {
    return null
  }

  const getPriorityColor = (priority) => {
    switch (priority) {
      case 'critical':
        return 'bg-red-100 border-red-400 text-red-900'
      case 'high':
        return 'bg-orange-100 border-orange-400 text-orange-900'
      case 'medium':
        return 'bg-yellow-100 border-yellow-400 text-yellow-900'
      case 'low':
        return 'bg-blue-100 border-blue-400 text-blue-900'
      default:
        return 'bg-gray-100 border-gray-400 text-gray-900'
    }
  }

  const getPriorityBadgeColor = (priority) => {
    switch (priority) {
      case 'critical':
        return 'bg-red-500 text-white'
      case 'high':
        return 'bg-orange-500 text-white'
      case 'medium':
        return 'bg-yellow-500 text-white'
      case 'low':
        return 'bg-blue-500 text-white'
      default:
        return 'bg-gray-500 text-white'
    }
  }

  const criticalGaps = skillGaps.filter(g => g.priority === 'critical')
  const otherGaps = skillGaps.filter(g => g.priority !== 'critical')

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <h3 className="text-2xl font-bold text-gray-900 mb-2">Smart Skill Gap Detection</h3>
      <p className="text-gray-600 mb-6">
        {skillGaps.length} skill gap{skillGaps.length !== 1 ? 's' : ''} identified
      </p>

      <div className="space-y-4">
        {/* Critical gaps first */}
        {criticalGaps.map((gap, idx) => (
          <div
            key={`critical-${idx}`}
            className={`border-l-4 rounded-lg p-4 ${getPriorityColor(gap.priority)}`}
          >
            <div className="flex items-start gap-3">
              <AlertTriangle className="w-5 h-5 flex-shrink-0 mt-1" />
              <div className="flex-1">
                <div className="flex items-center gap-2 mb-2">
                  <h4 className="text-lg font-bold">{gap.skillName}</h4>
                  <span className={`text-xs font-bold px-3 py-1 rounded-full ${getPriorityBadgeColor(gap.priority)}`}>
                    {gap.priority.toUpperCase()}
                  </span>
                </div>

                <div className="space-y-3">
                  <div>
                    <h5 className="text-sm font-semibold mb-1">Why It Matters</h5>
                    <p className="text-sm leading-relaxed">{gap.whyItMatters}</p>
                  </div>

                  <div>
                    <h5 className="text-sm font-semibold mb-1">Evidence Missing</h5>
                    <p className="text-sm leading-relaxed">{gap.evidenceMissing}</p>
                  </div>

                  <div className="bg-white bg-opacity-60 rounded p-2 border-l-2 border-current">
                    <h5 className="text-sm font-semibold mb-1 flex items-center gap-2">
                      <Zap className="w-4 h-4" />
                      How To Fix
                    </h5>
                    <p className="text-sm leading-relaxed">{gap.recommendation}</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        ))}

        {/* Other gaps */}
        {otherGaps.map((gap, idx) => (
          <div
            key={`other-${idx}`}
            className={`border-l-4 rounded-lg p-4 ${getPriorityColor(gap.priority)}`}
          >
            <div className="flex items-start gap-3">
              <CheckCircle2 className="w-5 h-5 flex-shrink-0 mt-1 opacity-60" />
              <div className="flex-1">
                <div className="flex items-center gap-2 mb-2">
                  <h4 className="text-lg font-bold">{gap.skillName}</h4>
                  <span className={`text-xs font-bold px-3 py-1 rounded-full ${getPriorityBadgeColor(gap.priority)}`}>
                    {gap.priority.toUpperCase()}
                  </span>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                  <div>
                    <h5 className="text-sm font-semibold mb-1">Why It Matters</h5>
                    <p className="text-sm leading-relaxed">{gap.whyItMatters}</p>
                  </div>

                  <div>
                    <h5 className="text-sm font-semibold mb-1">Evidence Missing</h5>
                    <p className="text-sm leading-relaxed">{gap.evidenceMissing}</p>
                  </div>
                </div>

                <div className="mt-3 bg-white bg-opacity-60 rounded p-2 border-l-2 border-current">
                  <h5 className="text-sm font-semibold mb-1 flex items-center gap-2">
                    <Zap className="w-4 h-4" />
                    Recommendation
                  </h5>
                  <p className="text-sm leading-relaxed">{gap.recommendation}</p>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
