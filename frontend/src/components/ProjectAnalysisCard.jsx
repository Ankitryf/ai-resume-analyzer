import { TrendingUp, AlertCircle, Lightbulb } from 'lucide-react'

export default function ProjectAnalysisCard({ projects }) {
  if (!projects || projects.length === 0) {
    return null
  }

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <h3 className="text-2xl font-bold text-gray-900 mb-6">Project Relevance Analysis</h3>
      
      <div className="space-y-6">
        {projects.map((project, idx) => (
          <div key={idx} className="border border-gray-200 rounded-lg p-5">
            <div className="flex items-start justify-between mb-4">
              <div>
                <h4 className="text-lg font-bold text-gray-900">{project.projectName}</h4>
              </div>
              <div className="text-right">
                <div className="text-sm font-semibold text-gray-700">Match</div>
                <div className={`text-3xl font-bold ${
                  project.matchPercentage >= 80 ? 'text-green-600' : 
                  project.matchPercentage >= 60 ? 'text-blue-600' : 
                  'text-yellow-600'
                }`}>
                  {Math.round(project.matchPercentage)}%
                </div>
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
              <div>
                <h5 className="text-sm font-semibold text-gray-700 mb-2 flex items-center gap-2">
                  <TrendingUp className="w-4 h-4 text-green-600" />
                  Relevant Skills
                </h5>
                <div className="flex flex-wrap gap-2">
                  {project.relevantSkills && project.relevantSkills.length > 0 ? (
                    project.relevantSkills.map((skill, i) => (
                      <span key={i} className="bg-green-100 text-green-800 text-xs font-semibold px-3 py-1 rounded-full">
                        {skill}
                      </span>
                    ))
                  ) : (
                    <span className="text-gray-500 text-sm">No relevant skills</span>
                  )}
                </div>
              </div>

              <div>
                <h5 className="text-sm font-semibold text-gray-700 mb-2 flex items-center gap-2">
                  <AlertCircle className="w-4 h-4 text-orange-600" />
                  Missing Skills
                </h5>
                <div className="flex flex-wrap gap-2">
                  {project.missingSkills && project.missingSkills.length > 0 ? (
                    project.missingSkills.map((skill, i) => (
                      <span key={i} className="bg-orange-100 text-orange-800 text-xs font-semibold px-3 py-1 rounded-full">
                        {skill}
                      </span>
                    ))
                  ) : (
                    <span className="text-gray-500 text-sm">No missing skills</span>
                  )}
                </div>
              </div>
            </div>

            {project.improvementSuggestions && project.improvementSuggestions.length > 0 && (
              <div className="bg-purple-50 border-l-4 border-purple-400 p-3 rounded">
                <h5 className="text-sm font-semibold text-purple-900 mb-2 flex items-center gap-2">
                  <Lightbulb className="w-4 h-4" />
                  Improvement Suggestions
                </h5>
                <ul className="text-sm text-purple-800 space-y-1">
                  {project.improvementSuggestions.map((suggestion, i) => (
                    <li key={i} className="flex items-start gap-2">
                      <span className="text-purple-600 mt-1">•</span>
                      <span>{suggestion}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  )
}
