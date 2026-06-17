import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { Upload, Loader } from 'lucide-react'
import client from '../api/client'

export default function AnalyzeResume() {
  const navigate = useNavigate()
  const [resume, setResume] = useState(null)
  const [jobDescription, setJobDescription] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const handleResumeChange = (e) => {
    const file = e.target.files[0]
    if (file && (file.type === 'application/pdf' || file.type === 'application/vnd.openxmlformats-officedocument.wordprocessingml.document')) {
      setResume(file)
      setError('')
    } else {
      setError('Please upload a valid PDF or DOCX file')
      setResume(null)
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!resume || !jobDescription.trim()) {
      setError('Please upload a resume and enter a job description')
      return
    }

    setLoading(true)
    setError('')

    try {
      const formData = new FormData()
      formData.append('resume', resume)
      formData.append('jobDescription', jobDescription)

      const response = await client.post('/analyze', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })

      navigate(`/results/${response.data.analysisId}`)
    } catch (err) {
      setError(err.response?.data?.detail || 'Analysis failed. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="max-w-3xl mx-auto">
      <div className="bg-white rounded-lg shadow-lg p-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-8">Analyze Your Resume</h1>

        {error && (
          <div className="bg-red-50 border border-red-200 text-red-800 px-4 py-3 rounded-lg mb-6">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-8">
          {/* Resume Upload */}
          <div>
            <label className="block text-lg font-semibold text-gray-900 mb-4">
              Upload Your Resume
            </label>
            <div className="relative border-2 border-dashed border-blue-300 rounded-lg p-8 text-center hover:border-blue-500 transition-colors">
              <input
                type="file"
                accept=".pdf,.docx"
                onChange={handleResumeChange}
                className="absolute inset-0 opacity-0 cursor-pointer"
              />
              <div className="space-y-2">
                <Upload className="w-12 h-12 text-blue-600 mx-auto" />
                <div>
                  <p className="text-blue-600 font-semibold">Click to upload or drag and drop</p>
                  <p className="text-gray-500 text-sm">PDF or DOCX (max 10MB)</p>
                </div>
              </div>
            </div>
            {resume && (
              <p className="text-green-600 text-sm mt-2">✓ {resume.name}</p>
            )}
          </div>

          {/* Job Description */}
          <div>
            <label htmlFor="jobDescription" className="block text-lg font-semibold text-gray-900 mb-4">
              Job Description
            </label>
            <textarea
              id="jobDescription"
              value={jobDescription}
              onChange={(e) => setJobDescription(e.target.value)}
              placeholder="Paste the job description here..."
              rows={10}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>

          {/* Submit Button */}
          <button
            type="submit"
            disabled={loading}
            className="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white font-bold py-3 rounded-lg transition-colors flex items-center justify-center gap-2"
          >
            {loading && <Loader className="w-5 h-5 animate-spin" />}
            {loading ? 'Analyzing...' : 'Analyze Resume'}
          </button>
        </form>
      </div>
    </div>
  )
}
