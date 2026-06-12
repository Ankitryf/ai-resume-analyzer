import React, { useState } from 'react';
import { ChevronDown, TrendingUp, AlertCircle, CheckCircle, User } from 'lucide-react';

const RecruiterSummaryCardV2 = ({ 
  hiringRecommendation = "Moderate Match",
  atsScore = 0,
  experienceMatch = 0,
  skillGapScore = 0,
  recruiterVerdict = "",
  readinessLevel = "",
  strengths = [],
  weaknesses = []
}) => {
  const [expandVerdict, setExpandVerdict] = useState(false);
  const [expandStrengths, setExpandStrengths] = useState(false);
  const [expandWeaknesses, setExpandWeaknesses] = useState(false);

  // Determine color based on hiring recommendation
  const getRecommendationColor = (rec) => {
    const lowercased = rec?.toLowerCase() || '';
    if (lowercased.includes('strong')) return { bg: 'bg-green-500', text: 'text-green-700', light: 'bg-green-100 text-green-700', title: '✓ Strong Match' };
    if (lowercased.includes('moderate')) return { bg: 'bg-blue-500', text: 'text-blue-700', light: 'bg-blue-100 text-blue-700', title: '◐ Moderate Match' };
    return { bg: 'bg-orange-500', text: 'text-orange-700', light: 'bg-orange-100 text-orange-700', title: '△ Needs Work' };
  };

  const getReadinessColor = (level) => {
    const lowercased = level?.toLowerCase() || '';
    if (lowercased.includes('ready') || lowercased.includes('excellent')) return 'text-green-700';
    if (lowercased.includes('good') || lowercased.includes('competitive')) return 'text-blue-700';
    if (lowercased.includes('fair') || lowercased.includes('develop')) return 'text-orange-700';
    return 'text-red-700';
  };

  const colors = getRecommendationColor(hiringRecommendation);

  // Calculate readiness percentage based on scores
  const overallReadiness = Math.round((atsScore * 0.3 + experienceMatch * 0.4 + (100 - skillGapScore) * 0.3) / 100 * 100);

  return (
    <div className="bg-white rounded-lg shadow-lg p-6 border-l-4" style={{ borderColor: colors.bg }}>
      {/* Header with Main Recommendation */}
      <div className="mb-6">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-2xl font-bold text-gray-800">Recruiter Evaluation</h3>
          <div className={`${colors.light} px-4 py-2 rounded-full font-bold text-sm`}>
            {colors.title}
          </div>
        </div>

        {/* Hiring Recommendation Card */}
        <div className={`${colors.bg} text-white p-4 rounded-lg shadow-md`}>
          <p className="text-sm font-semibold opacity-90 mb-1">HIRING RECOMMENDATION</p>
          <p className="text-xl font-bold">{hiringRecommendation || 'Moderate Match'}</p>
        </div>
      </div>

      {/* Score Summary Grid */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
        <div className="bg-gradient-to-br from-blue-50 to-blue-100 p-4 rounded-lg border border-blue-200">
          <p className="text-xs text-gray-600 font-semibold">ATS Score</p>
          <p className="text-3xl font-bold text-blue-700 mt-1">{Math.round(atsScore)}%</p>
          <p className="text-xs text-blue-600 mt-1">Keyword Match</p>
        </div>

        <div className="bg-gradient-to-br from-purple-50 to-purple-100 p-4 rounded-lg border border-purple-200">
          <p className="text-xs text-gray-600 font-semibold">Experience</p>
          <p className="text-3xl font-bold text-purple-700 mt-1">{Math.round(experienceMatch)}%</p>
          <p className="text-xs text-purple-600 mt-1">Match Score</p>
        </div>

        <div className="bg-gradient-to-br from-red-50 to-red-100 p-4 rounded-lg border border-red-200">
          <p className="text-xs text-gray-600 font-semibold">Skill Gaps</p>
          <p className="text-3xl font-bold text-red-700 mt-1">{Math.round(skillGapScore)}%</p>
          <p className="text-xs text-red-600 mt-1">Gap Score</p>
        </div>

        <div className="bg-gradient-to-br from-green-50 to-green-100 p-4 rounded-lg border border-green-200">
          <p className="text-xs text-gray-600 font-semibold">Overall</p>
          <p className="text-3xl font-bold text-green-700 mt-1">{overallReadiness}%</p>
          <p className="text-xs text-green-600 mt-1">Readiness</p>
        </div>
      </div>

      {/* Readiness Level */}
      {readinessLevel && (
        <div className="mb-6 p-4 bg-gradient-to-r from-gray-50 to-white border-l-4 border-gray-300 rounded">
          <p className="text-xs font-semibold text-gray-600 mb-1">READINESS LEVEL</p>
          <p className={`text-lg font-bold ${getReadinessColor(readinessLevel)}`}>
            {readinessLevel}
          </p>
        </div>
      )}

      {/* Recruiter Verdict */}
      {recruiterVerdict && (
        <div className="mb-6">
          <button
            onClick={() => setExpandVerdict(!expandVerdict)}
            className="w-full flex items-start justify-between bg-gradient-to-r from-gray-50 to-white p-4 rounded-lg border-2 border-gray-300 hover:bg-gray-100 transition-colors"
          >
            <div className="flex items-start gap-3 flex-1">
              <User size={20} className="text-gray-600 mt-1" />
              <div className="text-left">
                <p className="font-semibold text-gray-800">Detailed Recruiter Verdict</p>
                <p className="text-sm text-gray-600 mt-1 line-clamp-2">{recruiterVerdict}</p>
              </div>
            </div>
            <ChevronDown 
              size={20}
              className={`text-gray-600 transition-transform flex-shrink-0 ${expandVerdict ? 'rotate-180' : ''}`}
            />
          </button>

          {expandVerdict && (
            <div className="mt-2 p-4 bg-gray-50 border-2 border-gray-300 rounded-lg">
              <p className="text-sm text-gray-700 leading-relaxed">
                {recruiterVerdict}
              </p>
            </div>
          )}
        </div>
      )}

      {/* Strengths Section */}
      <div className="mb-4">
        <button
          onClick={() => setExpandStrengths(!expandStrengths)}
          className="w-full flex items-center justify-between bg-gradient-to-r from-green-50 to-white p-4 rounded-lg border-2 border-green-300 hover:bg-green-100 transition-colors"
        >
          <div className="flex items-center gap-3 flex-1">
            <CheckCircle size={20} className="text-green-600" />
            <span className="font-semibold text-gray-800">
              Key Strengths ({strengths.length})
            </span>
          </div>
          <ChevronDown 
            size={20}
            className={`text-green-600 transition-transform ${expandStrengths ? 'rotate-180' : ''}`}
          />
        </button>

        {expandStrengths && (
          <div className="mt-2 p-4 bg-green-50 border-2 border-green-300 rounded-lg space-y-3">
            {strengths && strengths.length > 0 ? (
              strengths.map((strength, idx) => (
                <div key={idx} className="flex items-start gap-3 p-3 bg-white rounded border border-green-200">
                  <CheckCircle size={18} className="text-green-600 mt-1 flex-shrink-0" />
                  <p className="text-sm text-gray-700">{strength}</p>
                </div>
              ))
            ) : (
              <p className="text-sm text-gray-600">No specific strengths identified yet.</p>
            )}
          </div>
        )}
      </div>

      {/* Weaknesses Section */}
      <div className="mb-6">
        <button
          onClick={() => setExpandWeaknesses(!expandWeaknesses)}
          className="w-full flex items-center justify-between bg-gradient-to-r from-orange-50 to-white p-4 rounded-lg border-2 border-orange-300 hover:bg-orange-100 transition-colors"
        >
          <div className="flex items-center gap-3 flex-1">
            <AlertCircle size={20} className="text-orange-600" />
            <span className="font-semibold text-gray-800">
              Areas for Improvement ({weaknesses.length})
            </span>
          </div>
          <ChevronDown 
            size={20}
            className={`text-orange-600 transition-transform ${expandWeaknesses ? 'rotate-180' : ''}`}
          />
        </button>

        {expandWeaknesses && (
          <div className="mt-2 p-4 bg-orange-50 border-2 border-orange-300 rounded-lg space-y-3">
            {weaknesses && weaknesses.length > 0 ? (
              weaknesses.map((weakness, idx) => (
                <div key={idx} className="flex items-start gap-3 p-3 bg-white rounded border border-orange-200">
                  <AlertCircle size={18} className="text-orange-600 mt-1 flex-shrink-0" />
                  <p className="text-sm text-gray-700">{weakness}</p>
                </div>
              ))
            ) : (
              <p className="text-sm text-gray-600">No significant weaknesses identified.</p>
            )}
          </div>
        )}
      </div>

      {/* Next Steps Button */}
      <div className="mt-6 pt-6 border-t border-gray-200">
        <button
          onClick={() => {
            const improvementsSection = document.getElementById('improvements-section');
            if (improvementsSection) {
              improvementsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
          }}
          className={`w-full ${colors.bg} text-white font-bold py-3 px-4 rounded-lg hover:opacity-90 transition-opacity text-lg`}
        >
          View Next Steps
        </button>
      </div>

      <div className="mt-4 p-4 bg-blue-50 border border-blue-200 rounded-lg">
        <p className="text-sm text-blue-900">
          <strong>💡 Pro Tip:</strong> Scroll down to see specific improvements, better resume bullets, and recommended projects to increase your chances of landing an interview.
        </p>
      </div>
    </div>
  );
};

export default RecruiterSummaryCardV2;
