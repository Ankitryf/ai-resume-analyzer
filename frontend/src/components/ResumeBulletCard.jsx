import { Copy, Download } from 'lucide-react'
import { useState } from 'react'

export default function ResumeBulletCard({ resumeBullets }) {
  const [copied, setCopied] = useState(null)

  if (!resumeBullets || resumeBullets.length === 0) {
    return null
  }

  const experienceBullets = resumeBullets.filter(b => b.section === 'Experience')
  const projectBullets = resumeBullets.filter(b => b.section === 'Projects')

  const copyToClipboard = (text, id) => {
    navigator.clipboard.writeText(text)
    setCopied(id)
    setTimeout(() => setCopied(null), 2000)
  }

  const BulletItem = ({ bullet, id }) => (
    <div className="bg-gray-50 border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
      <div className="flex items-start gap-3">
        <div className="flex-1">
          <p className="text-sm text-gray-700 leading-relaxed font-mono">
            • {bullet.bulletPoint}
          </p>
          <p className="text-xs text-gray-500 mt-2">
            Addresses: <span className="font-semibold text-gray-700">{bullet.skillGap}</span>
          </p>
        </div>
        <button
          onClick={() => copyToClipboard(bullet.bulletPoint, id)}
          className="flex-shrink-0 p-2 hover:bg-gray-200 rounded transition-colors"
          title="Copy to clipboard"
        >
          <Copy className={`w-4 h-4 ${copied === id ? 'text-green-600' : 'text-gray-600'}`} />
        </button>
      </div>
    </div>
  )

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <h3 className="text-2xl font-bold text-gray-900 mb-2">Resume Bullet Suggestions</h3>
      <p className="text-gray-600 mb-6">
        ATS-optimized bullet points to showcase acquired skills. Copy and paste these into your resume.
      </p>

      {experienceBullets.length > 0 && (
        <div className="mb-8">
          <h4 className="text-lg font-bold text-gray-900 mb-4 flex items-center gap-2">
            💼 Experience Section
          </h4>
          <div className="space-y-3">
            {experienceBullets.map((bullet, idx) => (
              <BulletItem
                key={`exp-${idx}`}
                bullet={bullet}
                id={`exp-${idx}`}
              />
            ))}
          </div>
        </div>
      )}

      {projectBullets.length > 0 && (
        <div className="mb-8">
          <h4 className="text-lg font-bold text-gray-900 mb-4 flex items-center gap-2">
            🚀 Projects Section
          </h4>
          <div className="space-y-3">
            {projectBullets.map((bullet, idx) => (
              <BulletItem
                key={`proj-${idx}`}
                bullet={bullet}
                id={`proj-${idx}`}
              />
            ))}
          </div>
        </div>
      )}

      <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
        <p className="text-sm text-blue-900">
          <strong>💡 Tip:</strong> These bullets are specifically designed to be ATS-friendly while naturally incorporating the skills missing from your current resume. Personalize them with your own achievements and metrics.
        </p>
      </div>
    </div>
  )
}
