import React, { useState } from 'react';
import { ChevronDown, Zap, Clock, Target, Star } from 'lucide-react';

const ProjectRecommendationCard = ({ 
  projectRecommendations = []
}) => {
  const [expandedIndex, setExpandedIndex] = useState(null);

  const getDifficultyColor = (difficulty) => {
    switch(difficulty?.toLowerCase()) {
      case 'beginner':
      case 'easy':
        return { bg: 'bg-green-100', text: 'text-green-700', label: 'Beginner' };
      case 'intermediate':
        return { bg: 'bg-blue-100', text: 'text-blue-700', label: 'Intermediate' };
      case 'advanced':
        return { bg: 'bg-purple-100', text: 'text-purple-700', label: 'Advanced' };
      case 'expert':
        return { bg: 'bg-red-100', text: 'text-red-700', label: 'Expert' };
      default:
        return { bg: 'bg-gray-100', text: 'text-gray-700', label: difficulty || 'Intermediate' };
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-6 border-l-4 border-purple-500">
      <div className="mb-6">
        <h3 className="text-2xl font-bold text-gray-800 mb-2">Recommended Projects</h3>
        <p className="text-gray-600 mb-4">
          Build these 2 projects to fill skill gaps and strengthen your profile
        </p>
      </div>

      {projectRecommendations && projectRecommendations.length > 0 ? (
        <div className="space-y-4">
          {projectRecommendations.map((project, idx) => {
            const isExpanded = expandedIndex === idx;
            const difficultyColor = getDifficultyColor(project.difficulty);
            const technologies = project.skillsLearned || project.technologies || [];
            
            return (
              <div
                key={idx}
                className="border-2 border-purple-200 rounded-lg overflow-hidden hover:shadow-lg transition-all duration-300"
              >
                <button
                  onClick={() => setExpandedIndex(isExpanded ? null : idx)}
                  className="w-full p-4 text-left bg-gradient-to-r from-purple-50 to-white hover:from-purple-100 transition-colors flex items-start justify-between gap-4"
                >
                  <div className="flex-1">
                    <div className="flex items-start justify-between gap-3 mb-2">
                      <h4 className="text-lg font-bold text-gray-800">
                        Project {idx + 1}: {project.projectName || project.title || `Recommended Project`}
                      </h4>
                      {idx === 0 && (
                        <span className="bg-yellow-400 text-yellow-900 px-2 py-1 rounded text-xs font-bold flex items-center gap-1">
                          <Star size={12} /> TOP PRIORITY
                        </span>
                      )}
                    </div>
                    
                    <div className="flex items-center gap-4 text-sm">
                      <div className={`${difficultyColor.bg} ${difficultyColor.text} px-3 py-1 rounded-full font-semibold text-xs`}>
                        {difficultyColor.label}
                      </div>
                      {project.estimatedTime && (
                        <div className="flex items-center gap-1 text-gray-600">
                          <Clock size={14} />
                          {project.estimatedTime}
                        </div>
                      )}
                    </div>

                    {technologies.length > 0 && (
                      <div className="flex flex-wrap gap-2 mt-3">
                        {technologies.slice(0, 3).map((tech, tidx) => (
                          <span key={tidx} className="bg-blue-100 text-blue-700 px-2 py-1 rounded text-xs font-semibold">
                            {tech}
                          </span>
                        ))}
                        {technologies.length > 3 && (
                          <span className="bg-gray-100 text-gray-700 px-2 py-1 rounded text-xs font-semibold">
                            +{technologies.length - 3} more
                          </span>
                        )}
                      </div>
                    )}
                  </div>

                  <ChevronDown 
                    size={20}
                    className={`flex-shrink-0 text-purple-600 transition-transform mt-1 ${isExpanded ? 'rotate-180' : ''}`}
                  />
                </button>

                {isExpanded && (
                  <div className="border-t-2 border-purple-200 p-4 bg-white space-y-4">
                    {/* Why It Fits */}
                    <div>
                      <h5 className="text-sm font-semibold text-gray-700 mb-2 flex items-center gap-2">
                        <Target size={16} className="text-purple-600" />
                        Why This Project Fits
                      </h5>
                      <p className="text-sm text-gray-700 bg-purple-50 p-3 rounded border border-purple-200">
                        {project.whyItFits || project.why_it_fits || project.why_recommended || 
                         "This project addresses the missing skills and requirements for your target role."}
                      </p>
                    </div>

                    {/* All Technologies */}
                    {technologies.length > 0 && (
                      <div>
                        <h5 className="text-sm font-semibold text-gray-700 mb-2 flex items-center gap-2">
                          <Zap size={16} className="text-purple-600" />
                          Skills You'll Learn
                        </h5>
                        <div className="flex flex-wrap gap-2">
                          {technologies.map((tech, tidx) => (
                            <span key={tidx} className="bg-gradient-to-r from-blue-100 to-blue-50 text-blue-700 px-3 py-1 rounded-full text-sm font-semibold border border-blue-200">
                              {tech}
                            </span>
                          ))}
                        </div>
                      </div>
                    )}

                    {/* Timeline & Difficulty */}
                    <div className="grid grid-cols-2 gap-4">
                      <div className="bg-gradient-to-br from-orange-50 to-orange-100 p-3 rounded border border-orange-200">
                        <p className="text-xs text-orange-700 font-semibold">Estimated Duration</p>
                        <p className="text-lg font-bold text-orange-700 mt-1">
                          {project.estimatedTime || project.duration || "4-6 weeks"}
                        </p>
                      </div>
                      <div className={`${difficultyColor.bg} p-3 rounded border-2 border-current`}>
                        <p className="text-xs font-semibold" style={{ color: difficultyColor.text.split('-')[1] }}>
                          Difficulty Level
                        </p>
                        <p className="text-lg font-bold mt-1" style={{ color: difficultyColor.text.split('-')[1] }}>
                          {difficultyColor.label}
                        </p>
                      </div>
                    </div>

                    {/* Implementation Tips */}
                    <div className="bg-blue-50 border border-blue-200 p-3 rounded">
                      <p className="text-xs font-semibold text-blue-900 mb-2">💡 Implementation Tips:</p>
                      <ul className="text-xs text-blue-800 space-y-1 list-disc list-inside">
                        <li>Document your architecture and decisions</li>
                        <li>Use GitHub for version control</li>
                        <li>Create a detailed README with screenshots</li>
                        <li>Deploy to showcase your work</li>
                      </ul>
                    </div>

                    {/* Impact Info */}
                    <div className="bg-green-50 border border-green-200 p-3 rounded">
                      <p className="text-xs font-semibold text-green-900">
                        ✓ Completing this project can improve your ATS score by 15-25%
                      </p>
                    </div>

                    {/* Action Buttons */}
                    <div className="flex gap-3 pt-3">
                      <button className="flex-1 bg-purple-600 hover:bg-purple-700 text-white font-semibold py-2 px-4 rounded transition-colors">
                        View Project Details
                      </button>
                      <button className="flex-1 bg-white border-2 border-purple-600 text-purple-600 hover:bg-purple-50 font-semibold py-2 px-4 rounded transition-colors">
                        Save Project
                      </button>
                    </div>
                  </div>
                )}
              </div>
            );
          })}
        </div>
      ) : (
        <div className="bg-gray-50 border-2 border-dashed border-gray-300 rounded-lg p-8 text-center">
          <p className="text-gray-600 mb-2">No projects needed!</p>
          <p className="text-sm text-gray-500">
            Your resume already covers the key requirements. However, building projects is always a great way to demonstrate your skills.
          </p>
        </div>
      )}

      <div className="mt-6 p-4 bg-purple-50 border border-purple-200 rounded-lg">
        <p className="text-sm text-purple-900">
          <strong>Expert Advice:</strong> These projects are specifically tailored to fill gaps in your profile. Completing even one of them will significantly improve your chances of landing interviews for this role.
        </p>
      </div>
    </div>
  );
};

export default ProjectRecommendationCard;
