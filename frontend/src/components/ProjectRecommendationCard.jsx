import { BookOpen, Clock, Award, Target } from 'lucide-react'

export default function ProjectRecommendationCard({ projects }) {
  if (!projects || projects.length === 0) {
    return null
  }

  const getDifficultyColor = (difficulty) => {
    switch (difficulty) {
      case 'beginner':
        return 'bg-green-100 text-green-800 border-green-300'
      case 'intermediate':
        return 'bg-blue-100 text-blue-800 border-blue-300'
      case 'advanced':
        return 'bg-purple-100 text-purple-800 border-purple-300'
      default:
        return 'bg-gray-100 text-gray-800 border-gray-300'
    }
  }

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <h3 className="text-2xl font-bold text-gray-900 mb-2">Recommended Projects</h3>
      <p className="text-gray-600 mb-6">Build these projects to acquire missing skills and improve your candidacy</p>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {projects.map((project, idx) => (
          <div key={idx} className="border border-gray-200 rounded-lg p-5 hover:shadow-lg transition-shadow">
            <div className="mb-4">
              <div className="flex items-center justify-between mb-3">
                <h4 className="text-lg font-bold text-gray-900">{project.projectName}</h4>
                <span className={`text-xs font-bold px-3 py-1 rounded-full border ${getDifficultyColor(project.difficulty)}`}>
                  {project.difficulty.toUpperCase()}
                </span>
              </div>

              <div className="flex items-center gap-4 text-sm text-gray-600 mb-4">
                <div className="flex items-center gap-2">
                  <Clock className="w-4 h-4 text-blue-600" />
                  <span>{project.estimatedTime}</span>
                </div>
                <div className="text-gray-400">•</div>
                <div className="flex items-center gap-2">
                  <Target className="w-4 h-4 text-purple-600" />
                  <span>Project #{project.order}</span>
                </div>
              </div>

              <div className="bg-yellow-50 border-l-4 border-yellow-400 p-3 rounded mb-4">
                <h5 className="text-sm font-semibold text-yellow-900 mb-2 flex items-center gap-2">
                  <Award className="w-4 h-4" />
                  Why It Fits This Job
                </h5>
                <p className="text-sm text-yellow-800 leading-relaxed">{project.whyItFits}</p>
              </div>
            </div>

            <div>
              <h5 className="text-sm font-bold text-gray-900 mb-2 flex items-center gap-2">
                <BookOpen className="w-4 h-4 text-indigo-600" />
                Skills You'll Learn
              </h5>
              <div className="flex flex-wrap gap-2">
                {project.skillsLearned && project.skillsLearned.length > 0 ? (
                  project.skillsLearned.map((skill, i) => (
                    <span key={i} className="bg-indigo-100 text-indigo-800 text-xs font-semibold px-3 py-1 rounded-full">
                      {skill}
                    </span>
                  ))
                ) : (
                  <span className="text-gray-500 text-sm">Skills will be determined by implementation</span>
                )}
              </div>
            </div>
          </div>
        ))}
      </div>

      <div className="mt-6 p-4 bg-blue-50 border border-blue-200 rounded-lg">
        <p className="text-sm text-blue-900">
          <strong>💡 Tip:</strong> Complete these projects, document your process, and add them to your resume and GitHub to strengthen your application.
        </p>
      </div>
    </div>
  )
}
