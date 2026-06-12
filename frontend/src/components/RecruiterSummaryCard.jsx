import { ThumbsUp, ThumbsDown, AlertCircle, Star } from 'lucide-react'

export default function RecruiterSummaryCard({
  hiringRecommendation,
  recruiterVerdict,
  strengths,
  weaknesses,
  improvementPriorities,
  experienceMatch,
  atsScore
}) {
  const getRecommendationColor = (rec) => {
    if (rec === 'Strong Match') return 'bg-green-100 border-green-400 text-green-900'
    if (rec === 'Moderate Match') return 'bg-blue-100 border-blue-400 text-blue-900'
    return 'bg-orange-100 border-orange-400 text-orange-900'
  }

  const getRecommendationIcon = (rec) => {
    if (rec === 'Strong Match') return '🎯'
    if (rec === 'Moderate Match') return '📊'
    return '⚠️'
  }

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <h3 className="text-2xl font-bold text-gray-900 mb-6">Recruiter Evaluation Summary</h3>

      {/* Hiring Recommendation */}
      <div className={`border-l-4 rounded-lg p-5 mb-6 ${getRecommendationColor(hiringRecommendation)}`}>
        <div className="flex items-center gap-3 mb-3">
          <span className="text-3xl">{getRecommendationIcon(hiringRecommendation)}</span>
          <div>
            <h4 className="text-sm font-semibold opacity-75">Hiring Recommendation</h4>
            <p className="text-2xl font-bold">{hiringRecommendation}</p>
          </div>
        </div>

        <div className="mt-4 pt-4 border-t border-current border-opacity-20">
          <h5 className="text-sm font-bold mb-2">Recruiter's Verdict</h5>
          <p className="text-sm leading-relaxed">{recruiterVerdict}</p>
        </div>
      </div>

      {/* Scores Summary */}
      <div className="grid grid-cols-2 gap-4 mb-6">
        <div className="bg-gradient-to-br from-blue-50 to-blue-100 rounded-lg p-4 border border-blue-200">
          <p className="text-sm text-blue-900 font-semibold mb-1">ATS Score</p>
          <p className="text-3xl font-bold text-blue-600">{atsScore.toFixed(0)}%</p>
        </div>
        <div className="bg-gradient-to-br from-purple-50 to-purple-100 rounded-lg p-4 border border-purple-200">
          <p className="text-sm text-purple-900 font-semibold mb-1">Experience Match</p>
          <p className="text-3xl font-bold text-purple-600">{experienceMatch.toFixed(0)}%</p>
        </div>
      </div>

      {/* Strengths and Weaknesses */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
        <div>
          <h4 className="text-lg font-bold text-gray-900 mb-3 flex items-center gap-2">
            <ThumbsUp className="w-5 h-5 text-green-600" />
            Key Strengths
          </h4>
          <ul className="space-y-2">
            {strengths && strengths.length > 0 ? (
              strengths.map((strength, idx) => (
                <li key={idx} className="flex items-start gap-3 text-sm">
                  <span className="text-green-600 font-bold mt-1">✓</span>
                  <span className="text-gray-700">{strength}</span>
                </li>
              ))
            ) : (
              <li className="text-gray-500 text-sm">No strengths identified</li>
            )}
          </ul>
        </div>

        <div>
          <h4 className="text-lg font-bold text-gray-900 mb-3 flex items-center gap-2">
            <ThumbsDown className="w-5 h-5 text-red-600" />
            Areas for Improvement
          </h4>
          <ul className="space-y-2">
            {weaknesses && weaknesses.length > 0 ? (
              weaknesses.map((weakness, idx) => (
                <li key={idx} className="flex items-start gap-3 text-sm">
                  <span className="text-red-600 font-bold mt-1">•</span>
                  <span className="text-gray-700">{weakness}</span>
                </li>
              ))
            ) : (
              <li className="text-gray-500 text-sm">No weaknesses identified</li>
            )}
          </ul>
        </div>
      </div>

      {/* Improvement Priorities */}
      <div className="bg-gradient-to-r from-indigo-50 to-purple-50 border border-indigo-200 rounded-lg p-5">
        <h4 className="text-lg font-bold text-gray-900 mb-4 flex items-center gap-2">
          <Star className="w-5 h-5 text-indigo-600" />
          Improvement Priority Roadmap
        </h4>

        <div className="space-y-3">
          {improvementPriorities && improvementPriorities.length > 0 ? (
            improvementPriorities.map((priority, idx) => (
              <div key={idx} className="flex items-start gap-3">
                <div className="flex items-center justify-center w-6 h-6 rounded-full bg-indigo-600 text-white text-sm font-bold flex-shrink-0">
                  {idx + 1}
                </div>
                <p className="text-sm text-gray-700 mt-0.5">{priority}</p>
              </div>
            ))
          ) : (
            <p className="text-gray-600 text-sm">No specific priorities available</p>
          )}
        </div>
      </div>

      {/* Call to Action */}
      <div className="mt-6 p-4 bg-green-50 border border-green-200 rounded-lg">
        <p className="text-sm text-green-900">
          <strong>📋 Next Steps:</strong> Review the skill gaps and project recommendations above, then work on the suggested improvements. These actions will directly address the hiring criteria for this role.
        </p>
      </div>
    </div>
  )
}
