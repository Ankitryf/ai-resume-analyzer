export default function SkillGapChart({ presentSkills, missingSkills }) {
  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <h3 className="text-xl font-bold text-gray-900 mb-6">Skill Gap Analysis</h3>
      
      <div className="space-y-6">
        <div>
          <h4 className="font-semibold text-green-600 mb-3">Present Skills ({presentSkills.length})</h4>
          <div className="flex flex-wrap gap-2">
            {presentSkills.map((skill, idx) => (
              <span
                key={idx}
                className="bg-green-100 text-green-800 px-3 py-1 rounded-full text-sm font-medium"
              >
                ✓ {skill}
              </span>
            ))}
          </div>
        </div>

        <div>
          <h4 className="font-semibold text-red-600 mb-3">Missing Skills ({missingSkills.length})</h4>
          <div className="flex flex-wrap gap-2">
            {missingSkills.map((skill, idx) => (
              <span
                key={idx}
                className="bg-red-100 text-red-800 px-3 py-1 rounded-full text-sm font-medium"
              >
                ✗ {skill}
              </span>
            ))}
          </div>
        </div>

        <div className="mt-6 p-4 bg-blue-50 rounded-lg">
          <div className="flex justify-between text-sm mb-2">
            <span className="font-medium">Skill Coverage</span>
            <span className="font-bold text-blue-600">
              {Math.round((presentSkills.length / (presentSkills.length + missingSkills.length)) * 100)}%
            </span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-3">
            <div
              className="bg-blue-600 h-3 rounded-full transition-all duration-300"
              style={{
                width: `${(presentSkills.length / (presentSkills.length + missingSkills.length)) * 100}%`
              }}
            />
          </div>
        </div>
      </div>
    </div>
  )
}
