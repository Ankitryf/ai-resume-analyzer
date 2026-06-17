import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { Loader, AlertCircle, Download, Share2 } from 'lucide-react';
import RecruiterSummaryCardV2 from '../components/RecruiterSummaryCardV2';
import KeywordSectionCard from '../components/KeywordSectionCard';
import ImprovedBulletsCard from '../components/ImprovedBulletsCard';
import ProjectRecommendationCardV2 from '../components/ProjectRecommendationCardV2';
import SkillGapCard from '../components/SkillGapCard';
import ExperienceAnalysisCard from '../components/ExperienceAnalysisCard';

const ResultsV2 = () => {
  const { analysisId } = useParams();
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchAnalysis = async () => {
      try {
        setLoading(true);
        const response = await fetch(`http://localhost:8000/api/analysis/${analysisId}`);
        
        if (!response.ok) {
          throw new Error('Failed to fetch analysis');
        }
        
        const data = await response.json();
        setAnalysis(data);
        setError(null);
      } catch (err) {
        setError(err.message);
        console.error('Error fetching analysis:', err);
      } finally {
        setLoading(false);
      }
    };

    if (analysisId) {
      fetchAnalysis();
    }
  }, [analysisId]);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen bg-gray-50">
        <div className="text-center">
          <Loader className="w-12 h-12 text-blue-600 animate-spin mx-auto mb-4" />
          <p className="text-gray-700 font-semibold">Analyzing your resume...</p>
          <p className="text-gray-500 text-sm mt-2">This may take a moment</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex items-center justify-center h-screen bg-gray-50">
        <div className="bg-white rounded-lg shadow-lg p-8 max-w-md">
          <AlertCircle className="w-12 h-12 text-red-600 mx-auto mb-4" />
          <h2 className="text-xl font-bold text-gray-800 mb-2">Error Loading Analysis</h2>
          <p className="text-gray-600 mb-4">{error}</p>
          <a href="/" className="text-blue-600 hover:underline">Back to Home</a>
        </div>
      </div>
    );
  }

  if (!analysis) {
    return (
      <div className="flex items-center justify-center h-screen bg-gray-50">
        <div className="text-center">
          <p className="text-gray-700 font-semibold">No analysis found</p>
          <a href="/" className="text-blue-600 hover:underline mt-2">Back to Home</a>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-50 to-gray-100">
      {/* Header */}
      <div className="bg-gradient-to-r from-blue-600 to-blue-800 text-white py-8 shadow-lg sticky top-0 z-40">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold">Resume Analysis Results</h1>
              <p className="text-blue-100 mt-1">AI-Powered Recruiter Evaluation</p>
            </div>
            <div className="flex gap-3">
              <button
                className="bg-white text-blue-600 hover:bg-blue-50 px-4 py-2 rounded-lg font-semibold flex items-center gap-2 transition-colors"
                onClick={() => window.print()}
              >
                <Download size={18} /> Download
              </button>
              <button
                className="bg-blue-700 hover:bg-blue-900 px-4 py-2 rounded-lg font-semibold flex items-center gap-2 transition-colors"
              >
                <Share2 size={18} /> Share
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Section 1: Recruiter Summary (Top Priority) */}
        <div className="mb-8">
          <RecruiterSummaryCardV2
            hiringRecommendation={analysis.hiringRecommendation}
            atsScore={analysis.atsScore}
            experienceMatch={analysis.experienceMatch}
            skillGapScore={analysis.skillGapScore}
            recruiterVerdict={analysis.recruiterVerdict}
            readinessLevel={analysis.readinessLevel}
            strengths={analysis.strengths}
            weaknesses={analysis.weaknesses}
          />
        </div>

        {/* Section 2: Experience Analysis */}
        {analysis.experienceAnalyses && analysis.experienceAnalyses.length > 0 && (
          <div className="mb-8">
            <ExperienceAnalysisCard
              experienceAnalyses={analysis.experienceAnalyses}
              experienceMatch={analysis.experienceMatch}
            />
          </div>
        )}

        {/* Section 3: Keyword Analysis */}
        <div className="mb-8">
          <KeywordSectionCard
            matchedKeywords={analysis.matchedKeywords}
            missingKeywords={analysis.missingKeywords}
            matchedCount={analysis.matchedKeywordCount}
            missingCount={analysis.missingKeywordCount}
          />
        </div>

        {/* Section 4: Skill Gaps */}
        {analysis.skillGaps && analysis.skillGaps.length > 0 && (
          <div className="mb-8">
            <SkillGapCard
              skillGaps={analysis.skillGaps}
              skillGapScore={analysis.skillGapScore}
            />
          </div>
        )}

        {/* Section 5: Improved Resume Bullets */}
        <div className="mb-8">
          <ImprovedBulletsCard
            improvedBullets={analysis.improvedBullets}
            skillGapCount={analysis.missingKeywordCount}
          />
        </div>

        {/* Section 6: Project Recommendations */}
        <div className="mb-8">
          <ProjectRecommendationCardV2
            projectRecommendations={analysis.projectRecommendations}
          />
        </div>

        {/* Improvements Section (Target for smooth scroll) */}
        <div id="improvements-section" className="mb-8 pt-8 border-t-4 border-gray-300">
          <h2 className="text-3xl font-bold text-gray-800 mb-6">📋 Improvement Checklist</h2>
          
          <div className="bg-white rounded-lg shadow-md p-6 border-l-4 border-yellow-500">
            <h3 className="text-xl font-bold text-gray-800 mb-4">Priority Actions</h3>
            
            <div className="space-y-4">
              {/* Priority 1: Keywords */}
              {analysis.missingKeywordCount > 0 && (
                <div className="flex items-start gap-4 p-4 bg-yellow-50 border border-yellow-200 rounded-lg">
                  <div className="bg-yellow-500 text-white rounded-full w-8 h-8 flex items-center justify-center font-bold flex-shrink-0">
                    1
                  </div>
                  <div className="flex-1">
                    <h4 className="font-semibold text-gray-800">Add Missing Keywords</h4>
                    <p className="text-sm text-gray-600 mt-1">
                      Incorporate {analysis.missingKeywordCount} missing keywords into your resume where relevant. 
                      See the keyword section above for the complete list.
                    </p>
                    <div className="mt-2 text-xs text-yellow-700 font-semibold">
                      ⏱️ Expected Impact: +15-20% ATS Score
                    </div>
                  </div>
                </div>
              )}

              {/* Priority 2: Improved Bullets */}
              {analysis.improvedBullets && analysis.improvedBullets.length > 0 && (
                <div className="flex items-start gap-4 p-4 bg-blue-50 border border-blue-200 rounded-lg">
                  <div className="bg-blue-500 text-white rounded-full w-8 h-8 flex items-center justify-center font-bold flex-shrink-0">
                    2
                  </div>
                  <div className="flex-1">
                    <h4 className="font-semibold text-gray-800">Update Resume Bullets</h4>
                    <p className="text-sm text-gray-600 mt-1">
                      Replace generic bullet points with the improved versions above. 
                      These are ATS-optimized and highlight quantifiable achievements.
                    </p>
                    <div className="mt-2 text-xs text-blue-700 font-semibold">
                      ⏱️ Expected Impact: +10-15% Interview Rate
                    </div>
                  </div>
                </div>
              )}

              {/* Priority 3: Projects */}
              {analysis.projectRecommendations && analysis.projectRecommendations.length > 0 && (
                <div className="flex items-start gap-4 p-4 bg-purple-50 border border-purple-200 rounded-lg">
                  <div className="bg-purple-500 text-white rounded-full w-8 h-8 flex items-center justify-center font-bold flex-shrink-0">
                    3
                  </div>
                  <div className="flex-1">
                    <h4 className="font-semibold text-gray-800">Build Recommended Projects</h4>
                    <p className="text-sm text-gray-600 mt-1">
                      Complete one or both recommended projects to demonstrate hands-on experience 
                      with the skills required for this role.
                    </p>
                    <div className="mt-2 text-xs text-purple-700 font-semibold">
                      ⏱️ Expected Impact: +25-30% Interview Rate
                    </div>
                  </div>
                </div>
              )}

              {/* Priority 4: Experience */}
              {analysis.experienceMatch < 80 && (
                <div className="flex items-start gap-4 p-4 bg-orange-50 border border-orange-200 rounded-lg">
                  <div className="bg-orange-500 text-white rounded-full w-8 h-8 flex items-center justify-center font-bold flex-shrink-0">
                    4
                  </div>
                  <div className="flex-1">
                    <h4 className="font-semibold text-gray-800">Enhance Experience Descriptions</h4>
                    <p className="text-sm text-gray-600 mt-1">
                      Your experience match score is {Math.round(analysis.experienceMatch)}%.
                      Add more details about relevant projects and responsibilities that align with the job.
                    </p>
                    <div className="mt-2 text-xs text-orange-700 font-semibold">
                      ⏱️ Expected Impact: +10-15% Interview Rate
                    </div>
                  </div>
                </div>
              )}
            </div>

            {/* Timeline */}
            <div className="mt-6 p-4 bg-green-50 border border-green-200 rounded-lg">
              <p className="text-sm font-semibold text-green-900 mb-2">📅 Recommended Timeline:</p>
              <ul className="text-sm text-green-800 space-y-1 list-disc list-inside">
                <li><strong>This week:</strong> Update keywords and bullet points (1-2 hours)</li>
                <li><strong>Next 2 weeks:</strong> Start building first recommended project</li>
                <li><strong>After project:</strong> Re-run analysis to verify improvements</li>
              </ul>
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="bg-white rounded-lg shadow-md p-6 text-center border-t-4 border-gray-300">
          <h3 className="text-xl font-bold text-gray-800 mb-2">Ready to improve your profile?</h3>
          <p className="text-gray-600 mb-4">
            Use the recommendations above to strengthen your resume and increase your chances of landing interviews.
          </p>
          <button
            onClick={() => window.location.href = '/'}
            className="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-6 rounded-lg transition-colors"
          >
            Analyze Another Resume
          </button>
        </div>
      </div>
    </div>
  );
};

export default ResultsV2;
