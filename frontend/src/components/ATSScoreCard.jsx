export default function ATSScoreCard({ score, details }) {
  const getScoreColor = (score) => {
    if (score >= 80) return 'text-green-600'
    if (score >= 60) return 'text-blue-600'
    if (score >= 40) return 'text-yellow-600'
    return 'text-red-600'
  }

  const getBgColor = (score) => {
    if (score >= 80) return 'bg-green-50 border-green-200'
    if (score >= 60) return 'bg-blue-50 border-blue-200'
    if (score >= 40) return 'bg-yellow-50 border-yellow-200'
    return 'bg-red-50 border-red-200'
  }

  return (
    <div className={`border-2 rounded-lg p-8 text-center ${getBgColor(score)}`}>
      <h2 className="text-gray-700 text-lg font-semibold mb-4">ATS Score</h2>
      <div className={`text-6xl font-bold ${getScoreColor(score)} mb-4`}>
        {score}%
      </div>
      {details && (
        <div className="text-sm text-gray-600 space-y-2">
          <p><strong>Keywords Matched:</strong> {details.keywordMatches}/{details.totalKeywords}</p>
          <p><strong>Format Score:</strong> {details.formatScore}%</p>
          <p><strong>Relevance:</strong> {details.relevance}%</p>
        </div>
      )}
    </div>
  )
}
