import google.generativeai as genai
import json
import re
from typing import List, Dict, Tuple, Optional
from app.config import settings
from app.nlp_utils import ResumeParser

class SemanticAnalyzer:
    """LLM-powered semantic analysis for intelligent resume evaluation"""
    
    def __init__(self):
        if settings.GEMINI_API_KEY:
            genai.configure(api_key=settings.GEMINI_API_KEY)
            self.model = genai.GenerativeModel('gemini-1.5-flash')
        else:
            self.model = None
    
    def infer_skills_from_content(self, resume_text: str, job_description: str) -> Tuple[List[str], Dict]:
        """Extract inferred skills from projects, experience, and certifications"""
        
        if not self.model:
            return [], {}
        
        prompt = f"""Analyze this resume and infer skills from the projects, work experience, certifications and descriptions.

RESUME:
{resume_text[:3000]}

For each project or work experience entry, extract the technical skills that can be inferred.

Return a JSON object with:
{{
    "inferred_skills": ["skill1", "skill2", ...],
    "skill_sources": {{
        "Backend Development": ["Built REST APIs using FastAPI and PostgreSQL"],
        "API Development": ["Built REST APIs using FastAPI and PostgreSQL"],
        ...
    }}
}}

Only return valid JSON, no additional text."""
        
        try:
            response = self.model.generate_content(prompt)
            result = json.loads(response.text)
            return result.get("inferred_skills", []), result.get("skill_sources", {})
        except Exception as e:
            print(f"Error inferring skills: {str(e)}")
            return [], {}
    
    def analyze_experience(self, resume_text: str, job_description: str) -> Tuple[float, List[str], List[str], str]:
        """Generate experience match score and analysis"""
        
        if not self.model:
            return 0.0, [], [], ""
        
        prompt = f"""Analyze the candidate's experience against this job description.

RESUME:
{resume_text[:3000]}

JOB DESCRIPTION:
{job_description[:2000]}

Evaluate:
1. How well does the candidate's experience match the role?
2. What are the key strengths?
3. What are the weaknesses?
4. Overall assessment

Return a JSON object:
{{
    "match_score": 85,
    "strengths": ["strength1", "strength2", "strength3"],
    "weaknesses": ["weakness1", "weakness2"],
    "assessment": "Paragraph explaining the candidate's suitability..."
}}

Only return valid JSON, no additional text."""
        
        try:
            response = self.model.generate_content(prompt)
            result = json.loads(response.text)
            return (
                result.get("match_score", 0) / 100.0,
                result.get("strengths", []),
                result.get("weaknesses", []),
                result.get("assessment", "")
            )
        except Exception as e:
            print(f"Error analyzing experience: {str(e)}")
            return 0.0, [], [], ""
    
    def analyze_projects(self, resume_text: str, job_description: str) -> List[Dict]:
        """Analyze each project in resume for relevance"""
        
        if not self.model:
            return []
        
        prompt = f"""Extract and analyze all projects from this resume.

RESUME:
{resume_text[:3000]}

JOB DESCRIPTION:
{job_description[:2000]}

For each project, return:
{{
    "projects": [
        {{
            "name": "Project Name",
            "match_percentage": 75,
            "relevant_skills": ["skill1", "skill2"],
            "missing_skills": ["skill3"],
            "improvement_suggestions": ["suggestion1", "suggestion2"]
        }}
    ]
}}

Only return valid JSON, no additional text."""
        
        try:
            response = self.model.generate_content(prompt)
            result = json.loads(response.text)
            return result.get("projects", [])
        except Exception as e:
            print(f"Error analyzing projects: {str(e)}")
            return []
    
    def identify_skill_gaps(self, resume_text: str, job_description: str) -> List[Dict]:
        """Identify critical skill gaps with reasoning"""
        
        if not self.model:
            return []
        
        prompt = f"""Identify skill gaps between candidate's resume and job requirements.

RESUME:
{resume_text[:3000]}

JOB DESCRIPTION:
{job_description[:2000]}

For each missing skill important for the role, explain:
1. Why it matters for this role
2. Evidence it's missing from resume
3. How to acquire it

Return a JSON array:
[
    {{
        "skill": "Cloud Deployment",
        "priority": "critical",
        "why_it_matters": "The role requires scalable production deployment.",
        "evidence_missing": "No AWS, Azure or GCP projects found.",
        "recommendation": "Deploy existing project to AWS and document architecture."
    }}
]

Only return valid JSON array, no additional text."""
        
        try:
            response = self.model.generate_content(prompt)
            result = json.loads(response.text)
            return result if isinstance(result, list) else []
        except Exception as e:
            print(f"Error identifying skill gaps: {str(e)}")
            return []
    
    def generate_resume_bullets(self, resume_text: str, skill_gaps: List[str]) -> List[Dict]:
        """Generate ATS-optimized bullet points for missing skills"""
        
        if not self.model or not skill_gaps:
            return []
        
        prompt = f"""Generate ATS-optimized resume bullet points for these missing skills.

CURRENT RESUME (for context):
{resume_text[:2000]}

MISSING SKILLS TO ADDRESS:
{', '.join(skill_gaps[:5])}

For each skill, create a realistic, ATS-optimized bullet point that:
1. Uses action verbs
2. Includes quantifiable results
3. Naturally incorporates the skill
4. Fits "Experience" or "Projects" section

Return JSON:
[
    {{
        "skill": "skill_name",
        "bullet": "Developed a containerized microservice architecture using Docker and Kubernetes, reducing deployment time by 40%.",
        "section": "Experience"
    }}
]

Only return valid JSON array, no additional text."""
        
        try:
            response = self.model.generate_content(prompt)
            result = json.loads(response.text)
            return result if isinstance(result, list) else []
        except Exception as e:
            print(f"Error generating bullets: {str(e)}")
            return []
    
    def recommend_projects(self, resume_text: str, skill_gaps: List[str], job_description: str) -> List[Dict]:
        """Generate 2 project recommendations to fill skill gaps"""
        
        if not self.model:
            return []
        
        prompt = f"""Generate exactly 2 projects to help the candidate acquire missing skills.

MISSING SKILLS:
{', '.join(skill_gaps[:5])}

JOB DESCRIPTION:
{job_description[:1500]}

For each project, provide:
1. Project name
2. Difficulty (beginner/intermediate/advanced)
3. Estimated time
4. Skills learned
5. Why it fits this specific job

Return JSON array with exactly 2 projects:
[
    {{
        "name": "Cloud-Native E-Commerce Platform",
        "difficulty": "intermediate",
        "estimated_time": "4-6 weeks",
        "skills_learned": ["AWS", "Docker", "CI/CD", "Microservices"],
        "why_it_fits": "Directly addresses missing cloud and deployment requirements."
    }},
    {{
        "name": "...",
        ...
    }}
]

Return only valid JSON array, no additional text."""
        
        try:
            response = self.model.generate_content(prompt)
            result = json.loads(response.text)
            return result if isinstance(result, list) else []
        except Exception as e:
            print(f"Error recommending projects: {str(e)}")
            return []
    
    def generate_recruiter_verdict(
        self,
        experience_match: float,
        strengths: List[str],
        weaknesses: List[str],
        ats_score: float,
        skill_gaps: List[Dict]
    ) -> Tuple[str, str, List[str]]:
        """Generate recruiter-style verdict and improvement priorities"""
        
        if not self.model:
            return "Moderate Match", "Candidate shows potential for this role.", ["Add missing skills", "Improve ATS score"]
        
        critical_gaps = len([g for g in skill_gaps if g.get("priority") == "critical"])
        
        prompt = f"""As a senior recruiter, evaluate this candidate.

PROFILE METRICS:
- Experience Match: {experience_match * 100:.0f}%
- ATS Score: {ats_score:.0f}%
- Critical Skill Gaps: {critical_gaps}
- Total Skill Gaps: {len(skill_gaps)}

STRENGTHS:
{json.dumps(strengths, indent=2)}

WEAKNESSES:
{json.dumps(weaknesses, indent=2)}

Provide:
1. Hiring recommendation (Strong Match / Moderate Match / Weak Match)
2. A paragraph verdict explaining suitability
3. Top 3 improvement priorities

Return JSON:
{{
    "recommendation": "Strong Match",
    "verdict": "Paragraph explaining why...",
    "priorities": ["Priority 1", "Priority 2", "Priority 3"]
}}

Only return valid JSON, no additional text."""
        
        try:
            response = self.model.generate_content(prompt)
            result = json.loads(response.text)
            return (
                result.get("recommendation", "Moderate Match"),
                result.get("verdict", "Candidate shows potential for this role."),
                result.get("priorities", [])
            )
        except Exception as e:
            print(f"Error generating verdict: {str(e)}")
            return "Moderate Match", "Candidate shows potential for this role.", ["Add missing skills", "Improve ATS score"]
