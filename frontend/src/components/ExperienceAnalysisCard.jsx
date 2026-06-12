import { CheckCircle, AlertCircle } from 'lucide-react'

export default function ExperienceAnalysisCard({ experiences }) {
  if (!experiences || experiences.length === 0) {
    return null
  }

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <h3 className="text-2xl font-bold text-gray-900 mb-6">Experience Analysis</h3>
      
      <div className="space-y-6">
        {experiences.map((exp, idx) => (
          <div key={idx} className="border border-gray-200 rounded-lg p-4">
            <div className="flex items-start justify-between mb-4">
              <div className="flex-1">
                <p className="text-sm text-gray-600 text-justify mb-2">
                  {exp.experienceEntry}
                </p>
              </div>
              <div className="ml-4 text-right">
                <div className="text-sm font-semibold text-gray-700">Match</div>
                <div className={`text-2xl font-bold ${
                  exp.matchScore >= 75 ? 'text-green-600' : 
                  exp.matchScore >= 50 ? 'text-yellow-600' : 
                  'text-red-600'
                }`}>
                  {Math.round(exp.matchScore)}%
                </div>
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
              <div>
                <h4 className="text-sm font-semibold text-green-700 mb-2 flex items-center gap-2">
                  <CheckCircle className="w-4 h-4" />
                  Relevant Skills
                </h4>
                <div className="flex flex-wrap gap-2">
                  {exp.relevantSkills && exp.relevantSkills.length > 0 ? (
                    exp.relevantSkills.map((skill, i) => (
                      <span key={i} className="bg-green-100 text-green-800 text-xs font-semibold px-3 py-1 rounded-full">
                        {skill}
                      </span>
                    ))
                  ) : (
                    <span className="text-gray-500 text-sm">No relevant skills identified</span>
                  )}
                </div>
              </div>

              <div>
                <h4 className="text-sm font-semibold text-red-700 mb-2 flex items-center gap-2">
                  <AlertCircle className="w-4 h-4" />
                  Missing Skills
                </h4>
                <div className="flex flex-wrap gap-2">
                  {exp.missingSkills && exp.missingSkills.length > 0 ? (
                    exp.missingSkills.map((skill, i) => (
                      <span key={i} className="bg-red-100 text-red-800 text-xs font-semibold px-3 py-1 rounded-full">
                        {skill}
                      </span>
                    ))
                  ) : (
                    <span className="text-gray-500 text-sm">No missing skills</span>
                  )}
                </div>
              </div>
            </div>

            <div className="bg-blue-50 border-l-4 border-blue-400 p-3 rounded">
              <p className="text-sm text-gray-700">
                <span className="font-semibold text-blue-900">Assessment:</span> {exp.assessment}
              </p>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
