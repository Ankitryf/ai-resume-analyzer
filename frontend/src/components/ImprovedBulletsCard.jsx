import React, { useState } from 'react';
import { ChevronDown, ArrowRight, TrendingUp } from 'lucide-react';

const ImprovedBulletsCard = ({ 
  improvedBullets = [],
  skillGapCount = 0
}) => {
  const [expandedIndex, setExpandedIndex] = useState(null);

  const getBulletTypeColor = (type) => {
    switch(type) {
      case 'achievement':
        return { bg: 'bg-blue-50', border: 'border-blue-200', text: 'text-blue-700', badge: 'bg-blue-100 text-blue-700' };
      case 'responsibility':
        return { bg: 'bg-purple-50', border: 'border-purple-200', text: 'text-purple-700', badge: 'bg-purple-100 text-purple-700' };
      case 'project':
        return { bg: 'bg-orange-50', border: 'border-orange-200', text: 'text-orange-700', badge: 'bg-orange-100 text-orange-700' };
      default:
        return { bg: 'bg-gray-50', border: 'border-gray-200', text: 'text-gray-700', badge: 'bg-gray-100 text-gray-700' };
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-6 border-l-4 border-orange-500">
      <div className="mb-6">
        <h3 className="text-2xl font-bold text-gray-800 mb-2">Resume Bullet Improvements</h3>
        <p className="text-gray-600 mb-4">
          Recruiter-optimized resume bullets that highlight missing skills and achievements
        </p>
        
        {improvedBullets.length > 0 && (
          <div className="inline-flex items-center gap-2 bg-orange-100 text-orange-800 px-4 py-2 rounded-full text-sm font-semibold">
            <TrendingUp size={16} />
            {improvedBullets.length} improvements available
          </div>
        )}
      </div>

      {improvedBullets.length > 0 ? (
        <div className="space-y-4">
          {improvedBullets.map((bullet, idx) => {
            const colors = getBulletTypeColor(bullet.type);
            const isExpanded = expandedIndex === idx;
            
            return (
              <div
                key={idx}
                className={`border-2 rounded-lg transition-all duration-300 ${colors.border} ${isExpanded ? colors.bg : 'bg-white'}`}
              >
                <button
                  onClick={() => setExpandedIndex(isExpanded ? null : idx)}
                  className={`w-full p-4 text-left flex items-start justify-between gap-4 hover:${colors.bg.replace('50', '100')} transition-colors`}
                >
                  <div className="flex-1">
                    <div className="flex items-center gap-2 mb-2">
                      <span className={`px-2 py-1 rounded text-xs font-semibold ${colors.badge}`}>
                        {bullet.type.charAt(0).toUpperCase() + bullet.type.slice(1)}
                      </span>
                      {bullet.impactMetric && (
                        <span className="text-xs bg-green-100 text-green-700 px-2 py-1 rounded font-semibold">
                          Impact: {bullet.impactMetric}
                        </span>
                      )}
                    </div>
                    <p className="text-sm text-gray-700 line-clamp-2">
                      {bullet.originalText}
                    </p>
                  </div>
                  <ChevronDown 
                    size={20}
                    className={`flex-shrink-0 text-gray-500 transition-transform ${isExpanded ? 'rotate-180' : ''}`}
                  />
                </button>

                {isExpanded && (
                  <div className={`border-t-2 p-4 space-y-4 ${colors.border}`}>
                    <div>
                      <h4 className="text-sm font-semibold text-gray-600 mb-2">Original Bullet Point:</h4>
                      <div className="bg-gray-50 p-3 rounded border border-gray-200 text-sm text-gray-700">
                        • {bullet.originalText}
                      </div>
                    </div>

                    <div className="flex items-center justify-center">
                      <div className="flex-1 h-px bg-gray-300"></div>
                      <ArrowRight size={20} className="text-gray-400 mx-3" />
                      <div className="flex-1 h-px bg-gray-300"></div>
                    </div>

                    <div>
                      <h4 className="text-sm font-semibold text-gray-600 mb-2">Improved Bullet Point:</h4>
                      <div className={`${colors.bg} p-3 rounded border-2 ${colors.border} text-sm ${colors.text} font-semibold`}>
                        • {bullet.improvedText}
                      </div>
                      <p className="text-xs text-gray-600 mt-2">
                        This version highlights quantifiable impact and uses ATS-friendly keywords. Customize as needed for your role.
                      </p>
                    </div>

                    {bullet.impactMetric && (
                      <div className="bg-blue-50 border border-blue-200 p-3 rounded">
                        <p className="text-xs font-semibold text-blue-900">
                          💡 Impact: {bullet.impactMetric}
                        </p>
                      </div>
                    )}

                    <button
                      onClick={() => {
                        navigator.clipboard.writeText(`• ${bullet.improvedText}`);
                        alert('Improved bullet copied to clipboard!');
                      }}
                      className={`w-full py-2 px-4 rounded font-semibold text-sm transition-colors ${colors.badge} hover:opacity-80`}
                    >
                      Copy to Clipboard
                    </button>
                  </div>
                )}
              </div>
            );
          })}
        </div>
      ) : (
        <div className="bg-gray-50 border-2 border-dashed border-gray-300 rounded-lg p-8 text-center">
          <p className="text-gray-600 mb-2">No improvements needed!</p>
          <p className="text-sm text-gray-500">
            Your resume already matches the job requirements well. Keep it as is or review the project recommendations section.
          </p>
        </div>
      )}

      <div className="mt-6 p-4 bg-blue-50 border border-blue-200 rounded-lg">
        <p className="text-sm text-blue-900">
          <strong>Pro Tip:</strong> Copy these improved bullets directly into your resume. Use numbers and metrics whenever possible to quantify your impact and improve ATS scores.
        </p>
      </div>
    </div>
  );
};

export default ImprovedBulletsCard;
