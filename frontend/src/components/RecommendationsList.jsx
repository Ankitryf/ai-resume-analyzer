import { CheckCircle, AlertCircle, Lightbulb } from 'lucide-react'

export default function RecommendationsList({ recommendations }) {
  const getPriorityColor = (priority) => {
    switch(priority) {
      case 'high': return 'border-red-200 bg-red-50'
      case 'medium': return 'border-yellow-200 bg-yellow-50'
      case 'low': return 'border-blue-200 bg-blue-50'
      default: return 'border-gray-200 bg-gray-50'
    }
  }

  const getPriorityIcon = (priority) => {
    switch(priority) {
      case 'high': return <AlertCircle className="w-5 h-5 text-red-600" />
      case 'medium': return <Lightbulb className="w-5 h-5 text-yellow-600" />
      default: return <CheckCircle className="w-5 h-5 text-blue-600" />
    }
  }

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <h3 className="text-xl font-bold text-gray-900 mb-6">AI-Powered Recommendations</h3>
      <div className="space-y-4">
        {recommendations && recommendations.map((rec, idx) => (
          <div key={idx} className={`border-2 rounded-lg p-4 ${getPriorityColor(rec.priority)}`}>
            <div className="flex gap-3 items-start">
              {getPriorityIcon(rec.priority)}
              <div className="flex-1">
                <h4 className="font-semibold text-gray-900">{rec.title}</h4>
                <p className="text-sm text-gray-700 mt-1">{rec.description}</p>
                {rec.action && (
                  <p className="text-sm font-medium text-gray-800 mt-2">
                    <strong>Action:</strong> {rec.action}
                  </p>
                )}
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
