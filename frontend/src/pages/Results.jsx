import { useParams, useNavigate } from 'react-router-dom'
import { useState, useEffect } from 'react'
import { Download, Loader, ArrowLeft } from 'lucide-react'
import client from '../api/client'
import ATSScoreCard from '../components/ATSScoreCard'
import ExperienceAnalysisCard from '../components/ExperienceAnalysisCard'
import ProjectAnalysisCard from '../components/ProjectAnalysisCard'
import SkillGapCard from '../components/SkillGapCard'
import ProjectRecommendationCard from '../components/ProjectRecommendationCard'
import ResumeBulletCard from '../components/ResumeBulletCard'
import RecruiterSummaryCard from '../components/RecruiterSummaryCard'
import RecommendationsList from '../components/RecommendationsList'

export default function Results() {
  const { analysisId } = useParams()
  const navigate = useNavigate()
  const [analysis, setAnalysis] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    const fetchResults = async () => {
      try {
        const response = await client.get(`/analysis/${analysisId}`)
        setAnalysis(response.data)
      } catch (err) {
        setError('Failed to load results. Please try again.')
      } finally {
        setLoading(false)
      }
    }

    fetchResults()
  }, [analysisId])

  const handleDownloadReport = async () => {
    try {
      const response = await client.get(`/analysis/${analysisId}/report`, {
        responseType: 'blob'
      })
      const url = window.URL.createObjectURL(new Blob([response.data]))
      const link = document.createElement('a')
      link.href = url
      link.setAttribute('download', `resume-analysis-${analysisId}.pdf`)
      document.body.appendChild(link)
      link.click()
      link.parentElement.removeChild(link)
    } catch (err) {
      alert('Failed to download report')
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-96">
        <div className="text-center">
          <Loader className="w-12 h-12 text-blue-600 animate-spin mx-auto mb-4" />
          <p className="text-gray-600">Analyzing your resume with AI intelligence...</p>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="bg-red-50 border border-red-200 text-red-800 px-6 py-4 rounded-lg">
        {error}
      </div>
    )
  }

  if (!analysis) {
    return <div className="text-center text-gray-600">No results found</div>
  }

  return (
    <div className="space-y-8">
      {/* Navigation */}
      <div className="flex items-center gap-4">
        <button
          onClick={() => navigate('/')}
          className="flex items-center gap-2 text-blue-600 hover:text-blue-700 font-medium"
        >
          <ArrowLeft className="w-5 h-5" />
          Back to Home
        </button>
        <button
          onClick={handleDownloadReport}
          className="ml-auto flex items-center gap-2 bg-green-600 hover:bg-green-700 text-white font-bold py-2 px-4 rounded-lg transition-colors"
        >
          <Download className="w-5 h-5" />
          Download Report
        </button>
      </div>

      {/* Main Scores Section */}
      <div className="bg-white rounded-lg shadow-md p-8">
        <h2 className="text-3xl font-bold text-center text-gray-900 mb-8">Resume Analysis Complete</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <ATSScoreCard
            score={analysis.atsScore}
            details={{
              keywordMatches: analysis.keywordMatches?.length || 0,
              totalKeywords: analysis.totalKeywords,
              formatScore: analysis.formatScore,
              relevance: analysis.relevance
            }}
          />
          <div className="bg-gradient-to-br from-purple-50 to-blue-50 rounded-lg p-8 text-center border-2 border-purple-200">
            <h2 className="text-gray-700 text-lg font-semibold mb-4">Experience Match</h2>
            <div className="text-6xl font-bold text-purple-600 mb-4">
              {analysis.experienceMatch.toFixed(0)}%
            </div>
            <p className="text-sm text-gray-600">
              Your experience aligns with the job requirements
            </p>
          </div>
        </div>
      </div>

      {/* Recruiter Summary - Key Section */}
      <RecruiterSummaryCard
        hiringRecommendation={analysis.hiringRecommendation}
        recruiterVerdict={analysis.recruiterVerdict}
        strengths={analysis.strengths}
        weaknesses={analysis.weaknesses}
        improvementPriorities={analysis.improvementPriorities}
        experienceMatch={analysis.experienceMatch}
        atsScore={analysis.atsScore}
      />

      {/* Experience Analysis */}
      <ExperienceAnalysisCard experiences={analysis.experienceAnalyses} />

      {/* Project Analysis */}
      <ProjectAnalysisCard projects={analysis.projectAnalyses} />

      {/* Skill Gap Detection */}
      <SkillGapCard skillGaps={analysis.skillGaps} />

      {/* Resume Bullet Suggestions */}
      <ResumeBulletCard resumeBullets={analysis.resumeBullets} />

      {/* Project Recommendations */}
      <ProjectRecommendationCard projects={analysis.projectRecommendations} />

      {/* Legacy Recommendations for backward compatibility */}
      {analysis.recommendations && analysis.recommendations.length > 0 && (
        <>
          <div className="border-t-2 border-gray-300 pt-8">
            <h3 className="text-2xl font-bold text-gray-900 mb-6">Additional AI Recommendations</h3>
          </div>
          <RecommendationsList recommendations={analysis.recommendations} />
        </>
      )}

      {/* Analysis Summary */}
      <div className="bg-gradient-to-r from-blue-50 to-cyan-50 border-l-4 border-blue-600 rounded-lg p-6">
        <h3 className="text-xl font-bold text-gray-900 mb-4">Summary</h3>
        <p className="text-gray-700 leading-relaxed">
          {analysis.summary || 'Your resume has been analyzed. Review the insights above to understand your strengths, identify skill gaps, and follow the recommended improvement roadmap.'}
        </p>
      </div>
    </div>
  )
}
