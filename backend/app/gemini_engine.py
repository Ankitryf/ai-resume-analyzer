import google.generativeai as genai
from typing import List, Dict
from app.config import settings

class GeminiRecommendationEngine:
    def __init__(self):
        if settings.GEMINI_API_KEY:
            genai.configure(api_key=settings.GEMINI_API_KEY)
            self.model = genai.GenerativeModel('gemini-pro')
        else:
            self.model = None

    def generate_recommendations(
        self,
        resume_text: str,
        job_description: str,
        missing_skills: List[str],
        missing_keywords: List[str],
        ats_score: float
    ) -> List[Dict]:
        """Generate AI-powered recommendations using Gemini API"""
        
        if not self.model:
            return self._get_default_recommendations(missing_skills, missing_keywords, ats_score)
        
        try:
            prompt = self._build_prompt(
                resume_text,
                job_description,
                missing_skills,
                missing_keywords,
                ats_score
            )
            
            response = self.model.generate_content(prompt)
            recommendations = self._parse_response(response.text)
            return recommendations
        except Exception as e:
            print(f"Error generating recommendations: {str(e)}")
            return self._get_default_recommendations(missing_skills, missing_keywords, ats_score)

    def _build_prompt(
        self,
        resume_text: str,
        job_description: str,
        missing_skills: List[str],
        missing_keywords: List[str],
        ats_score: float
    ) -> str:
        """Build the prompt for Gemini API"""
        
        prompt = f"""
Analyze this resume and job description to provide actionable recommendations:

RESUME (First 2000 chars):
{resume_text[:2000]}

JOB DESCRIPTION (First 2000 chars):
{job_description[:2000]}

Current ATS Score: {ats_score}%
Missing Skills: {', '.join(missing_skills[:10])}
Missing Keywords: {', '.join(missing_keywords[:10])}

Provide 5-7 specific, actionable recommendations to improve the resume's ATS score and relevance.
For each recommendation, include:
1. Title
2. Description
3. Specific action to take
4. Priority (high/medium/low)

Format the response as a list of JSON objects with keys: title, description, action, priority
"""
        return prompt

    def _parse_response(self, response_text: str) -> List[Dict]:
        """Parse Gemini response into recommendation format"""
        recommendations = []
        
        try:
            import json
            import re
            
            # Extract JSON objects from response
            json_pattern = r'\{[^{}]*\}'
            matches = re.findall(json_pattern, response_text)
            
            for match in matches:
                try:
                    rec = json.loads(match)
                    if 'title' in rec and 'description' in rec:
                        recommendations.append({
                            'title': rec.get('title', ''),
                            'description': rec.get('description', ''),
                            'action': rec.get('action', ''),
                            'priority': rec.get('priority', 'medium'),
                            'category': rec.get('category', 'general')
                        })
                except json.JSONDecodeError:
                    continue
            
        except Exception as e:
            print(f"Error parsing response: {str(e)}")
        
        # If no recommendations parsed, return default ones
        if not recommendations:
            return self._get_default_recommendations([], [], 0)
        
        return recommendations[:7]  # Limit to 7 recommendations

    @staticmethod
    def _get_default_recommendations(
        missing_skills: List[str],
        missing_keywords: List[str],
        ats_score: float
    ) -> List[Dict]:
        """Return default recommendations when Gemini is unavailable"""
        
        recommendations = []
        
        # Skill-based recommendations
        if missing_skills:
            for skill in missing_skills[:3]:
                recommendations.append({
                    'title': f'Add {skill} Experience',
                    'description': f'The job requires {skill} but it\'s not mentioned in your resume.',
                    'action': f'Add a bullet point highlighting your {skill} experience or projects.',
                    'priority': 'high',
                    'category': 'skills'
                })
        
        # Keyword-based recommendations
        if missing_keywords:
            recommendations.append({
                'title': 'Include Missing Keywords',
                'description': f'Add keywords like {", ".join(missing_keywords[:5])} that appear in the job description.',
                'action': 'Naturally incorporate these keywords throughout your resume.',
                'priority': 'high',
                'category': 'keywords'
            })
        
        # ATS score recommendations
        if ats_score < 60:
            recommendations.append({
                'title': 'Improve Resume Format',
                'description': 'Your ATS score is below 60%, which may cause issues with automated screening.',
                'action': 'Use standard formatting, consistent fonts, and ATS-friendly structure.',
                'priority': 'high',
                'category': 'format'
            })
        
        # Content recommendations
        recommendations.append({
            'title': 'Enhance Achievement Descriptions',
            'description': 'Provide quantifiable results and metrics for your accomplishments.',
            'action': 'Replace vague descriptions with specific numbers and outcomes.',
            'priority': 'medium',
            'category': 'content'
        })
        
        return recommendations
