import React, { useState } from 'react';
import { ChevronDown } from 'lucide-react';

const KeywordSectionCard = ({ 
  matchedKeywords = [], 
  missingKeywords = [],
  matchedCount = 0,
  missingCount = 0
}) => {
  const [expandMatched, setExpandMatched] = useState(false);
  const [expandMissing, setExpandMissing] = useState(false);

  const totalKeywords = matchedCount + missingCount;
  const matchPercentage = totalKeywords > 0 ? ((matchedCount / totalKeywords) * 100).toFixed(0) : 0;

  return (
    <div className="bg-white rounded-lg shadow-md p-6 border-l-4 border-blue-500">
      <div className="mb-6">
        <h3 className="text-2xl font-bold text-gray-800 mb-2">Keyword Analysis</h3>
        <p className="text-gray-600 mb-4">ATS keyword matching breakdown</p>
        
        {/* Summary Stats */}
        <div className="grid grid-cols-3 gap-4 mb-6">
          <div className="bg-gradient-to-br from-green-50 to-green-100 p-4 rounded-lg">
            <div className="text-3xl font-bold text-green-600">{matchedCount}</div>
            <div className="text-sm text-gray-700">Matched Keywords</div>
            <div className="text-xs text-green-600 font-semibold">{matchPercentage}% Match</div>
          </div>
          <div className="bg-gradient-to-br from-red-50 to-red-100 p-4 rounded-lg">
            <div className="text-3xl font-bold text-red-600">{missingCount}</div>
            <div className="text-sm text-gray-700">Missing Keywords</div>
            <div className="text-xs text-red-600 font-semibold">{100 - matchPercentage}% Gap</div>
          </div>
          <div className="bg-gradient-to-br from-blue-50 to-blue-100 p-4 rounded-lg">
            <div className="text-3xl font-bold text-blue-600">{totalKeywords}</div>
            <div className="text-sm text-gray-700">Total Keywords</div>
            <div className="text-xs text-blue-600 font-semibold">Job Requirements</div>
          </div>
        </div>

        {/* Match Percentage Bar */}
        <div className="w-full bg-gray-200 rounded-full h-3 overflow-hidden">
          <div 
            className="bg-gradient-to-r from-green-400 to-green-600 h-full transition-all duration-500"
            style={{ width: `${matchPercentage}%` }}
          ></div>
        </div>
        <div className="text-sm text-gray-600 mt-2">
          {matchPercentage}% of job requirements keywords found in your resume
        </div>
      </div>

      {/* Matched Keywords Collapsible */}
      <div className="mb-4">
        <button
          onClick={() => setExpandMatched(!expandMatched)}
          className="w-full flex items-center justify-between bg-green-50 p-4 rounded-lg border border-green-200 hover:bg-green-100 transition-colors"
        >
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 bg-green-500 text-white rounded-full flex items-center justify-center text-sm font-bold">
              ✓
            </div>
            <span className="font-semibold text-gray-800">
              Matched Keywords ({matchedCount})
            </span>
          </div>
          <ChevronDown 
            size={20}
            className={`text-green-600 transition-transform ${expandMatched ? 'rotate-180' : ''}`}
          />
        </button>
        
        {expandMatched && (
          <div className="mt-2 p-4 bg-green-50 rounded-lg border border-green-200">
            <div className="flex flex-wrap gap-2">
              {matchedKeywords && matchedKeywords.length > 0 ? (
                matchedKeywords.map((keyword, idx) => (
                  <span
                    key={idx}
                    className="inline-flex items-center gap-2 bg-green-500 text-white px-3 py-1 rounded-full text-sm font-medium"
                  >
                    <span>✓</span>
                    {keyword}
                  </span>
                ))
              ) : (
                <p className="text-gray-600">No matched keywords available</p>
              )}
            </div>
            <p className="text-xs text-gray-600 mt-3">
              These keywords appear in both your resume and the job description, improving your ATS score.
            </p>
          </div>
        )}
      </div>

      {/* Missing Keywords Collapsible */}
      <div>
        <button
          onClick={() => setExpandMissing(!expandMissing)}
          className="w-full flex items-center justify-between bg-red-50 p-4 rounded-lg border border-red-200 hover:bg-red-100 transition-colors"
        >
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 bg-red-500 text-white rounded-full flex items-center justify-center text-sm font-bold">
              ✗
            </div>
            <span className="font-semibold text-gray-800">
              Missing Keywords ({missingCount})
            </span>
          </div>
          <ChevronDown 
            size={20}
            className={`text-red-600 transition-transform ${expandMissing ? 'rotate-180' : ''}`}
          />
        </button>
        
        {expandMissing && (
          <div className="mt-2 p-4 bg-red-50 rounded-lg border border-red-200">
            <div className="flex flex-wrap gap-2">
              {missingKeywords && missingKeywords.length > 0 ? (
                missingKeywords.map((keyword, idx) => (
                  <span
                    key={idx}
                    className="inline-flex items-center gap-2 bg-red-500 text-white px-3 py-1 rounded-full text-sm font-medium"
                  >
                    <span>✗</span>
                    {keyword}
                  </span>
                ))
              ) : (
                <p className="text-gray-600">No missing keywords</p>
              )}
            </div>
            <p className="text-xs text-gray-600 mt-3">
              These keywords are in the job description but missing from your resume. Consider adding them where relevant to improve ATS score.
            </p>
          </div>
        )}
      </div>
    </div>
  );
};

export default KeywordSectionCard;
