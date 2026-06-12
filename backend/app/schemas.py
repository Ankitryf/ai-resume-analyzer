from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from datetime import datetime

# User Schemas
class UserBase(BaseModel):
    email: EmailStr
    username: str
    full_name: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

# Resume Schemas
class ResumeResponse(BaseModel):
    id: int
    filename: str
    created_at: datetime
    
    class Config:
        from_attributes = True

# Keyword Match Schemas
class KeywordMatchResponse(BaseModel):
    keyword: str
    frequency: int
    
    class Config:
        from_attributes = True

# Missing Skill Schemas
class MissingSkillResponse(BaseModel):
    skill_name: str
    importance: str
    
    class Config:
        from_attributes = True

# Recommendation Schemas
class RecommendationResponse(BaseModel):
    title: str
    description: str
    action: str
    priority: str
    category: str
    
    class Config:
        from_attributes = True

# New Recruiter-Style Schemas

class ExperienceAnalysisResponse(BaseModel):
    experience_entry: str
    match_score: float
    relevant_skills: List[str]
    missing_skills: List[str]
    assessment: str
    
    class Config:
        from_attributes = True

class ProjectAnalysisResponse(BaseModel):
    project_name: str
    match_percentage: float
    relevant_skills: List[str]
    missing_skills: List[str]
    improvement_suggestions: List[str]
    
    class Config:
        from_attributes = True

class SkillGapResponse(BaseModel):
    skill_name: str
    why_it_matters: str
    evidence_missing: str
    recommendation: str
    priority: str
    
    class Config:
        from_attributes = True

class ProjectRecommendationResponse(BaseModel):
    project_name: str
    difficulty: str
    estimated_time: str
    skills_learned: List[str]
    why_it_fits: str
    order: int
    
    class Config:
        from_attributes = True

class ResumeBulletResponse(BaseModel):
    skill_gap: str
    bullet_point: str
    section: str
    
    class Config:
        from_attributes = True

# Analysis Result Schemas
class ImprovedBulletResponse(BaseModel):
    original_text: str
    improved_text: str
    impact_metric: Optional[str]
    type: str
    
    class Config:
        from_attributes = True

class AnalysisResultResponse(BaseModel):
    id: int
    ats_score: float
    format_score: float
    relevance_score: float
    experience_match_score: float
    experience_match_explanation: Optional[str]
    summary: Optional[str]
    recruiter_verdict: Optional[str]
    hiring_recommendation: str
    readiness_level: str
    strengths: List[str]
    weaknesses: List[str]
    improvement_priorities: List[str]
    inferred_skills: List[str]
    matched_keywords: List[str]
    missing_keywords: List[str]
    matched_keyword_count: int
    missing_keyword_count: int
    skill_gap_score: float
    created_at: datetime
    resume: ResumeResponse
    keyword_matches: List[KeywordMatchResponse]
    missing_skills: List[MissingSkillResponse]
    recommendations: List[RecommendationResponse]
    experience_analyses: List[ExperienceAnalysisResponse]
    project_analyses: List[ProjectAnalysisResponse]
    skill_gaps: List[SkillGapResponse]
    project_recommendations: List[ProjectRecommendationResponse]
    resume_bullets: List[ResumeBulletResponse]
    improved_bullets: List[ImprovedBulletResponse]
    
    class Config:
        from_attributes = True

class AnalysisRequest(BaseModel):
    resume: str = Field(..., description="Base64 encoded resume content or file path")
    jobDescription: str = Field(..., description="Job description text")

# Authentication Schemas
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    username: Optional[str] = None

class LoginRequest(BaseModel):
    username: str
    password: str
