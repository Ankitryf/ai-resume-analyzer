from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Float,
    DateTime,
    ForeignKey,
    Boolean,
    JSON,
    ARRAY,
)
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    full_name = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = Column(DateTime, nullable=True)

    # Relationships
    resumes = relationship(
        "Resume", back_populates="user", cascade="all, delete-orphan"
    )
    analyses = relationship(
        "AnalysisResult", back_populates="user", cascade="all, delete-orphan"
    )


class Resume(Base):
    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    filename = Column(String)
    file_path = Column(String)
    original_text = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = Column(DateTime, nullable=True)

    # Relationships
    user = relationship("User", back_populates="resumes")
    sections = relationship(
        "ResumeSection", back_populates="resume", cascade="all, delete-orphan"
    )
    analyses = relationship("AnalysisResult", back_populates="resume")


class ResumeSection(Base):
    __tablename__ = "resume_sections"

    id = Column(Integer, primary_key=True, index=True)
    resume_id = Column(Integer, ForeignKey("resumes.id"), nullable=False)
    section_name = Column(String)  # e.g., "Education", "Experience", "Skills"
    content = Column(Text)

    resume = relationship("Resume", back_populates="sections")


class JobDescription(Base):
    __tablename__ = "job_descriptions"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    deleted_at = Column(DateTime, nullable=True)


class AnalysisResult(Base):
    __tablename__ = "analysis_results"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    resume_id = Column(Integer, ForeignKey("resumes.id"), nullable=False)
    job_description_id = Column(
        Integer, ForeignKey("job_descriptions.id"), nullable=True
    )
    ats_score = Column(Float)
    format_score = Column(Float)
    relevance_score = Column(Float)
    summary = Column(Text)

    # Enhanced recruiter-style fields
    experience_match_score = Column(Float, default=0.0)
    experience_match_explanation = Column(Text, nullable=True)
    recruiter_verdict = Column(Text, nullable=True)
    hiring_recommendation = Column(
        String
    )  # "Strong Match", "Moderate Match", "Weak Match"
    readiness_level = Column(
        String
    )  # "Ready Now", "Ready with Projects", "Needs More Work"
    strengths = Column(JSON, default=[])
    weaknesses = Column(JSON, default=[])
    improvement_priorities = Column(JSON, default=[])
    inferred_skills = Column(JSON, default=[])

    # Keyword analysis fields
    matched_keywords = Column(JSON, default=[])
    missing_keywords = Column(JSON, default=[])
    matched_keyword_count = Column(Integer, default=0)
    missing_keyword_count = Column(Integer, default=0)

    # Skill gap score (0-100)
    skill_gap_score = Column(Float, default=0.0)

    created_at = Column(DateTime, default=datetime.utcnow)
    deleted_at = Column(DateTime, nullable=True)

    # Relationships
    user = relationship("User", back_populates="analyses")
    resume = relationship("Resume", back_populates="analyses")
    job_description = relationship("JobDescription")
    keyword_matches = relationship(
        "KeywordMatch", back_populates="analysis", cascade="all, delete-orphan"
    )
    missing_skills = relationship(
        "MissingSkill", back_populates="analysis", cascade="all, delete-orphan"
    )
    recommendations = relationship(
        "Recommendation", back_populates="analysis", cascade="all, delete-orphan"
    )
    experience_analyses = relationship(
        "ExperienceAnalysis", back_populates="analysis", cascade="all, delete-orphan"
    )
    project_analyses = relationship(
        "ProjectAnalysis", back_populates="analysis", cascade="all, delete-orphan"
    )
    skill_gaps = relationship(
        "SkillGap", back_populates="analysis", cascade="all, delete-orphan"
    )
    project_recommendations = relationship(
        "ProjectRecommendation", back_populates="analysis", cascade="all, delete-orphan"
    )
    resume_bullets = relationship(
        "ResumeBullet", back_populates="analysis", cascade="all, delete-orphan"
    )
    improved_bullets = relationship(
        "ImprovedBullet", back_populates="analysis", cascade="all, delete-orphan"
    )


class Skill(Base):
    __tablename__ = "skills"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    category = Column(String)  # e.g., "Programming", "Database", "Framework"


class KeywordMatch(Base):
    __tablename__ = "keyword_matches"

    id = Column(Integer, primary_key=True, index=True)
    analysis_id = Column(Integer, ForeignKey("analysis_results.id"), nullable=False)
    keyword = Column(String)
    frequency = Column(Integer, default=1)

    analysis = relationship("AnalysisResult", back_populates="keyword_matches")


class MissingSkill(Base):
    __tablename__ = "missing_skills"

    id = Column(Integer, primary_key=True, index=True)
    analysis_id = Column(Integer, ForeignKey("analysis_results.id"), nullable=False)
    skill_name = Column(String)
    importance = Column(String)  # "high", "medium", "low"

    analysis = relationship("AnalysisResult", back_populates="missing_skills")


class Recommendation(Base):
    __tablename__ = "recommendations"

    id = Column(Integer, primary_key=True, index=True)
    analysis_id = Column(Integer, ForeignKey("analysis_results.id"), nullable=False)
    title = Column(String)
    description = Column(Text)
    action = Column(String)
    priority = Column(String)  # "high", "medium", "low"
    category = Column(String)  # "content", "format", "skills", "keywords"

    analysis = relationship("AnalysisResult", back_populates="recommendations")


# New models for recruiter-style evaluation


class ExperienceAnalysis(Base):
    __tablename__ = "experience_analyses"

    id = Column(Integer, primary_key=True, index=True)
    analysis_id = Column(Integer, ForeignKey("analysis_results.id"), nullable=False)
    experience_entry = Column(Text)  # Original experience text from resume
    match_score = Column(Float)  # 0-100
    relevant_skills = Column(JSON, default=[])
    missing_skills = Column(JSON, default=[])
    assessment = Column(Text)  # AI assessment of this experience

    analysis = relationship("AnalysisResult", back_populates="experience_analyses")


class ProjectAnalysis(Base):
    __tablename__ = "project_analyses"

    id = Column(Integer, primary_key=True, index=True)
    analysis_id = Column(Integer, ForeignKey("analysis_results.id"), nullable=False)
    project_name = Column(String)
    match_percentage = Column(Float)  # 0-100
    relevant_skills = Column(JSON, default=[])
    missing_skills = Column(JSON, default=[])
    improvement_suggestions = Column(JSON, default=[])

    analysis = relationship("AnalysisResult", back_populates="project_analyses")


class SkillGap(Base):
    __tablename__ = "skill_gaps"

    id = Column(Integer, primary_key=True, index=True)
    analysis_id = Column(Integer, ForeignKey("analysis_results.id"), nullable=False)
    skill_name = Column(String)
    why_it_matters = Column(Text)  # Why this skill is important for the role
    evidence_missing = Column(Text)  # Why we don't see this skill in resume
    recommendation = Column(Text)  # How to acquire this skill
    priority = Column(String)  # "critical", "high", "medium", "low"

    analysis = relationship("AnalysisResult", back_populates="skill_gaps")


class ProjectRecommendation(Base):
    __tablename__ = "project_recommendations"

    id = Column(Integer, primary_key=True, index=True)
    analysis_id = Column(Integer, ForeignKey("analysis_results.id"), nullable=False)
    project_name = Column(String)
    difficulty = Column(String)  # "beginner", "intermediate", "advanced"
    estimated_time = Column(String)  # e.g., "2-3 weeks"
    skills_learned = Column(JSON, default=[])
    why_it_fits = Column(Text)  # Explanation of relevance to job
    order = Column(Integer)  # 1 or 2

    analysis = relationship("AnalysisResult", back_populates="project_recommendations")


class ResumeBullet(Base):
    __tablename__ = "resume_bullets"

    id = Column(Integer, primary_key=True, index=True)
    analysis_id = Column(Integer, ForeignKey("analysis_results.id"), nullable=False)
    skill_gap = Column(String)  # Which skill gap this addresses
    bullet_point = Column(Text)  # ATS-optimized bullet suggestion
    section = Column(String)  # "Experience" or "Projects"

    analysis = relationship("AnalysisResult", back_populates="resume_bullets")


class ImprovedBullet(Base):
    __tablename__ = "improved_bullets"

    id = Column(Integer, primary_key=True, index=True)
    analysis_id = Column(Integer, ForeignKey("analysis_results.id"), nullable=False)
    original_text = Column(Text)  # Original bullet from resume
    improved_text = Column(Text)  # Improved, recruiter-friendly version
    impact_metric = Column(String, nullable=True)  # e.g., "60% faster", "10K+ users"
    type = Column(String)  # "achievement", "responsibility", "project"

    analysis = relationship("AnalysisResult", back_populates="improved_bullets")
