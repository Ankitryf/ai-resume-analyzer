import google.generativeai as genai
import json
import re
from typing import List, Dict, Tuple, Optional
from app.config import settings
from app.nlp_utils import ResumeParser

class EnhancedSemanticAnalyzer:
    """LLM-powered semantic analysis for recruiter-style resume evaluation"""
    
    def __init__(self):
        if settings.GEMINI_API_KEY:
            genai.configure(api_key=settings.GEMINI_API_KEY)
            self.model = genai.GenerativeModel('gemini-1.5-flash')
        else:
            self.model = None
    
    # ============ CORE ANALYSIS METHODS ============
    
    def analyze_experience_match(self, resume_text: str, job_description: str) -> Tuple[float, str, List[str], List[str]]:
        """Analyze experience match semantically (not just keywords)"""
        
        if not self.model:
            return 0.0, "Experience analysis unavailable", [], []
        
        prompt = f"""Analyze the candidate's experience against this job role semantically.

RESUME:
{resume_text[:3000]}

JOB DESCRIPTION:
{job_description[:2000]}

Evaluate:
1. Do their projects align with job requirements?
2. Do their technologies match what's needed?
3. Do their responsibilities match the role?
4. Calculate overall match as percentage (0-100)

Return JSON:
{{
    "match_score": 75,
    "explanation": "Candidate has strong backend experience with similar tech stack...",
    "matched_areas": ["Backend development", "Database design"],
    "gaps": ["Cloud deployment", "Kubernetes"]
}}

Only return valid JSON."""
        
        try:
            response = self.model.generate_content(prompt)
            result = json.loads(response.text)
            return (
                result.get("match_score", 0) / 100.0,
                result.get("explanation", ""),
                result.get("matched_areas", []),
                result.get("gaps", [])
            )
        except Exception as e:
            print(f"Error analyzing experience: {str(e)}")
            return 0.0, "Analysis error", [], []
    
    def generate_strengths_weaknesses(self, 
                                     resume_text: str, 
                                     job_description: str,
                                     matched_keywords: List[str],
                                     missing_keywords: List[str]) -> Tuple[List[str], List[str]]:
        """Generate meaningful strengths and weaknesses"""
        
        if not self.model:
            return [], []
        
        prompt = f"""Based on this resume and job description, generate meaningful strengths and weaknesses.

RESUME:
{resume_text[:2500]}

JOB DESCRIPTION:
{job_description[:1500]}

MATCHED KEYWORDS: {', '.join(matched_keywords[:10])}
MISSING KEYWORDS: {', '.join(missing_keywords[:10])}

Analyze semantically and return:
{{
    "strengths": [
        "Strong backend development experience with production systems",
        "Experience with modern tech stack (Python, FastAPI, PostgreSQL)",
        ...
    ],
    "weaknesses": [
        "Limited cloud infrastructure experience",
        "No demonstrated DevOps skills",
        ...
    ]
}}

Be specific and meaningful. Max 5 each."""
        
        try:
            response = self.model.generate_content(prompt)
            result = json.loads(response.text)
            return result.get("strengths", []), result.get("weaknesses", [])
        except Exception as e:
            print(f"Error generating strengths/weaknesses: {str(e)}")
            return [], []
    
    def generate_improved_bullets(self, resume_text: str, job_description: str) -> List[Dict]:
        """Generate improved, recruiter-friendly resume bullets with quantification"""
        
        if not self.model:
            return []
        
        prompt = f"""Improve this resume's experience bullets to be more recruiter-friendly and quantified.

RESUME:
{resume_text[:3000]}

JOB DESCRIPTION:
{job_description[:1500]}

For each work experience or project in the resume:
1. Identify the key achievement
2. Quantify the impact (speed, performance, savings, etc.)
3. Align with job requirements
4. Make it recruiter-friendly

Return JSON array:
[
    {{
        "original": "Built REST APIs",
        "improved": "Architected and deployed 12+ REST APIs serving 10K+ daily requests with 99.9% uptime",
        "type": "achievement"
    }},
    {{
        "original": "Managed database",
        "improved": "Optimized PostgreSQL queries reducing response time by 60% for million+ record datasets",
        "type": "achievement"
    }}
]

Focus on impact and metrics."""
        
        try:
            response = self.model.generate_content(prompt)
            result = json.loads(response.text)
            return result if isinstance(result, list) else []
        except Exception as e:
            print(f"Error improving bullets: {str(e)}")
            return []
    
    def generate_project_recommendations(self, 
                                        resume_text: str, 
                                        job_description: str,
                                        skill_gaps: List[str]) -> List[Dict]:
        """Generate 2 detailed project recommendations with ATS impact"""
        
        if not self.model:
            return []
        
        prompt = f"""Generate 2 specific projects to help this candidate win the job.

CANDIDATE SUMMARY:
{resume_text[:2000]}

TARGET JOB:
{job_description[:1500]}

SKILL GAPS:
{', '.join(skill_gaps[:5])}

For each project:
1. Address specific job requirements
2. Build real, impressive portfolio piece
3. Estimate ATS improvement

Return exactly 2 projects:
[
    {{
        "title": "Distributed Task Queue with Celery & Redis",
        "difficulty": "intermediate",
        "duration": "3-4 weeks",
        "technologies": ["Python", "Celery", "Redis", "Docker"],
        "why_recommended": "Job requires scalability and async processing experience",
        "skills_gained": ["Async patterns", "Message queues", "Caching"],
        "ats_improvement": 12,
        "description": "Build a production-ready task queue system..."
    }},
    ...
]

Each project increases ATS match by X% based on job fit."""
        
        try:
            response = self.model.generate_content(prompt)
            result = json.loads(response.text)
            return result if isinstance(result, list) else []
        except Exception as e:
            print(f"Error generating projects: {str(e)}")
            return []
    
    def generate_recruiter_verdict(self,
                                  experience_match: float,
                                  strengths: List[str],
                                  weaknesses: List[str],
                                  ats_score: float,
                                  skill_gaps: List[str]) -> Tuple[str, str, str]:
        """Generate detailed recruiter verdict with recommendation"""
        
        if not self.model:
            return "Moderate Match", "Candidate shows potential", "Ready with improvements"
        
        prompt = f"""As a senior recruiter, provide a verdict on this candidate.

PROFILE:
- Experience Match: {experience_match * 100:.0f}%
- ATS Score: {ats_score:.0f}%
- Key Strengths: {', '.join(strengths[:3])}
- Key Weaknesses: {', '.join(weaknesses[:3])}
- Critical Gaps: {len([g for g in skill_gaps if 'critical' in g.lower()])}
- Total Gaps: {len(skill_gaps)}

Provide assessment:
{{
    "recommendation": "Strong Match / Moderate Match / Weak Match",
    "verdict": "Paragraph (3-4 sentences) explaining suitability, strengths, concerns",
    "readiness": "Ready Now / Ready with Projects / Needs More Work"
}}

Be honest but constructive."""
        
        try:
            response = self.model.generate_content(prompt)
            result = json.loads(response.text)
            return (
                result.get("recommendation", "Moderate Match"),
                result.get("verdict", ""),
                result.get("readiness", "Ready with Projects")
            )
        except Exception as e:
            print(f"Error generating verdict: {str(e)}")
            return "Moderate Match", "Assessment unavailable", "Needs evaluation"
    
    def generate_keyword_analysis(self, resume_text: str, job_description: str) -> Tuple[List[str], List[str], int, int]:
        """Semantic keyword analysis (not just string matching)"""
        
        if not self.model:
            return [], [], 0, 0
        
        prompt = f"""Extract keywords semantically from resume and job description.

RESUME:
{resume_text[:2500]}

JOB DESCRIPTION:
{job_description[:1500]}

Find:
1. Technical keywords in resume
2. Technical keywords needed in job
3. Semantic matches (e.g., "PostgreSQL" matches "SQL database" requirement)
4. Meaningful missing keywords

Return:
{{
    "matched": ["Python", "FastAPI", "PostgreSQL"],
    "missing": ["Kubernetes", "CI/CD"],
    "matched_count": 15,
    "missing_count": 8
}}

Focus on meaningful technical terms."""
        
        try:
            response = self.model.generate_content(prompt)
            result = json.loads(response.text)
            return (
                result.get("matched", []),
                result.get("missing", []),
                result.get("matched_count", 0),
                result.get("missing_count", 0)
            )
        except Exception as e:
            print(f"Error in keyword analysis: {str(e)}")
            return [], [], 0, 0
    
    # ============ HELPER METHODS ============
    
    def calculate_skill_gap_score(self, missing_count: int, matched_count: int) -> float:
        """Calculate skill gap score (0-100)"""
        total = missing_count + matched_count
        if total == 0:
            return 0.0
        return (matched_count / total) * 100
    
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


class SemanticAnalyzer(EnhancedSemanticAnalyzer):
    """Backward compatibility wrapper"""
    pass
