import { Link } from 'react-router-dom'
import { Upload, BarChart3, Sparkles } from 'lucide-react'

export default function Dashboard() {
  return (
    <div className="space-y-12">
      {/* Hero Section */}
      <section className="text-center py-12">
        <h1 className="text-5xl font-bold text-white mb-4">
          AI Resume Analyzer
        </h1>
        <p className="text-xl text-gray-300 mb-8 max-w-2xl mx-auto">
          Optimize your resume for ATS systems, identify skill gaps, and get AI-powered recommendations to land your dream job.
        </p>
        <Link
          to="/analyze"
          className="inline-block bg-blue-600 hover:bg-blue-700 text-white font-bold py-4 px-8 rounded-lg text-lg transition-colors"
        >
          Start Analyzing Now
        </Link>
      </section>

      {/* Features Section */}
      <section>
        <h2 className="text-3xl font-bold text-white mb-8 text-center">How It Works</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {/* Feature 1 */}
          <div className="bg-white rounded-lg shadow-lg p-8 hover:shadow-xl transition-shadow">
            <Upload className="w-12 h-12 text-blue-600 mb-4" />
            <h3 className="text-xl font-bold text-gray-900 mb-3">Upload & Match</h3>
            <p className="text-gray-600">
              Upload your resume and job description. Our AI analyzes the match instantly.
            </p>
          </div>

          {/* Feature 2 */}
          <div className="bg-white rounded-lg shadow-lg p-8 hover:shadow-xl transition-shadow">
            <BarChart3 className="w-12 h-12 text-green-600 mb-4" />
            <h3 className="text-xl font-bold text-gray-900 mb-3">Get ATS Score</h3>
            <p className="text-gray-600">
              Receive a detailed ATS compatibility score and understand what recruiters see.
            </p>
          </div>

          {/* Feature 3 */}
          <div className="bg-white rounded-lg shadow-lg p-8 hover:shadow-xl transition-shadow">
            <Sparkles className="w-12 h-12 text-purple-600 mb-4" />
            <h3 className="text-xl font-bold text-gray-900 mb-3">Smart Suggestions</h3>
            <p className="text-gray-600">
              Get actionable AI recommendations to improve your resume and chances.
            </p>
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="bg-white rounded-lg shadow-lg p-12">
        <h2 className="text-3xl font-bold text-gray-900 mb-8 text-center">Why Choose Us?</h2>
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8 text-center">
          <div>
            <div className="text-4xl font-bold text-blue-600 mb-2">50K+</div>
            <p className="text-gray-600">Resumes Analyzed</p>
          </div>
          <div>
            <div className="text-4xl font-bold text-green-600 mb-2">92%</div>
            <p className="text-gray-600">ATS Success Rate</p>
          </div>
          <div>
            <div className="text-4xl font-bold text-purple-600 mb-2">98%</div>
            <p className="text-gray-600">User Satisfaction</p>
          </div>
          <div>
            <div className="text-4xl font-bold text-orange-600 mb-2">2M+</div>
            <p className="text-gray-600">Keywords Analyzed</p>
          </div>
        </div>
      </section>
    </div>
  )
}
