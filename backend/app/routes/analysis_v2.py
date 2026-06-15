from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
import uuid
import os

from app.database import get_db
from app.models import (
    AnalysisResult, Resume, JobDescription, KeywordMatch, MissingSkill, Recommendation,
    ExperienceAnalysis, ProjectAnalysis, SkillGap, ProjectRecommendation, ResumeBullet, ImprovedBullet
)
from app.schemas import AnalysisResultResponse
from app.nlp_utils import ResumeParser, KeywordExtractor, ATSScorer
from app.gemini_engine import GeminiRecommendationEngine
from app.semantic_analyzer_v2 import EnhancedSemanticAnalyzer
from app.config import settings

router = APIRouter()

@router.post("/analyze")
async def analyze_resume(
    resume: UploadFile = File(...),
    jobDescription: str = Form(...),
    db: Session = Depends(get_db)
):
    """Comprehensive resume analysis with recruiter-style evaluation"""
    
    try:
        # Read resume file
        resume_content = await resume.read()
        
        # Parse resume
        resume_text = ResumeParser.parse_resume(resume_content, resume.filename)
        
        # Extract keywords (legacy + semantic)
        matching_keywords, missing_keywords = KeywordExtractor.extract_keywords(
            resume_text, 
            jobDescription
        )
        
        # Extract skills (legacy)
        present_skills = KeywordExtractor.extract_skills(resume_text)
        required_skills = KeywordExtractor.extract_skills(jobDescription)
        missing_skills = [s for s in required_skills if s not in present_skills]
        
        # Calculate ATS score
        ats_score = ATSScorer.calculate_score(
            resume_text,
            jobDescription,
            matching_keywords,
            len(matching_keywords) + len(missing_keywords),
            present_skills,
            len(required_skills)
        )
        
        # ============ ENHANCED SEMANTIC ANALYSIS ============
        analyzer = EnhancedSemanticAnalyzer()
        
        # 1. Analyze experience match semantically
        exp_match, exp_explanation, matched_areas, gaps = analyzer.analyze_experience_match(
            resume_text, jobDescription
        )
        
        # 2. Generate meaningful strengths and weaknesses
        strengths, weaknesses = analyzer.generate_strengths_weaknesses(
            resume_text, jobDescription, matching_keywords, missing_keywords
        )
        
        # 3. Generate improved resume bullets
        improved_bullets_data = analyzer.generate_improved_bullets(resume_text, jobDescription)
        
        # 4. Generate project recommendations (2 projects with details)
        project_recommendations = analyzer.generate_project_recommendations(
            resume_text, jobDescription, [s for s in missing_skills]
        )
        
        # 5. Generate recruiter verdict
        recommendation, verdict, readiness = analyzer.generate_recruiter_verdict(
            exp_match, strengths, weaknesses, ats_score, missing_skills
        )
        
        # 6. Semantic keyword analysis
        matched_kw, missing_kw, matched_count, missing_count = analyzer.generate_keyword_analysis(
            resume_text, jobDescription
        )
        
        # 7. Calculate skill gap score
        skill_gap_score = analyzer.calculate_skill_gap_score(missing_count, matched_count)
        
        # Legacy recommendations
        recommendation_engine = GeminiRecommendationEngine()
        recommendations = recommendation_engine.generate_recommendations(
            resume_text,
            jobDescription,
            missing_skills,
            missing_keywords,
            ats_score
        )
        
        # ============ SAVE TO DATABASE ============
        
        job_desc_obj = JobDescription(
            title="Job Description",
            content=jobDescription
        )
        db.add(job_desc_obj)
        db.flush()
        
        resume_obj = Resume(
            user_id=1,  # TODO: Get from current user
            filename=resume.filename,
            file_path=f"uploads/{uuid.uuid4()}_{resume.filename}",
            original_text=resume_text
        )
        db.add(resume_obj)
        db.flush()
        
        analysis = AnalysisResult(
            user_id=1,  # TODO: Get from current user
            resume_id=resume_obj.id,
            job_description_id=job_desc_obj.id,
            ats_score=ats_score,
            format_score=ATSScorer.evaluate_format(resume_text),
            relevance_score=len(matching_keywords) / max(1, len(matching_keywords) + len(missing_keywords)) * 100,
            experience_match_score=exp_match * 100,
            experience_match_explanation=exp_explanation,
            summary=f"Your resume has an ATS score of {ats_score}%. Experience match: {exp_match * 100:.0f}%",
            recruiter_verdict=verdict,
            hiring_recommendation=recommendation,
            readiness_level=readiness,
            strengths=strengths,
            weaknesses=weaknesses,
            improvement_priorities=[],  # Will be populated below
            inferred_skills=present_skills,
            matched_keywords=matched_kw,
            missing_keywords=missing_kw,
            matched_keyword_count=matched_count,
            missing_keyword_count=missing_count,
            skill_gap_score=skill_gap_score
        )
        db.add(analysis)
        db.flush()
        
        # Save keyword matches
        for keyword in matching_keywords:
            km = KeywordMatch(analysis_id=analysis.id, keyword=keyword)
            db.add(km)
        
        # Save missing skills
        for skill in missing_skills:
            ms = MissingSkill(
                analysis_id=analysis.id,
                skill_name=skill,
                importance="high" if skill in missing_keywords else "medium"
            )
            db.add(ms)
        
        # Save recommendations (legacy)
        for rec in recommendations:
            r = Recommendation(
                analysis_id=analysis.id,
                title=rec.get('title', ''),
                description=rec.get('description', ''),
                action=rec.get('action', ''),
                priority=rec.get('priority', 'medium'),
                category=rec.get('category', 'general')
            )
            db.add(r)
        
        # Save improved bullets
        for bullet in improved_bullets_data:
            ib = ImprovedBullet(
                analysis_id=analysis.id,
                original_text=bullet.get('original', ''),
                improved_text=bullet.get('improved', ''),
                impact_metric=bullet.get('metric'),
                type=bullet.get('type', 'achievement')
            )
            db.add(ib)
        
        # Save project recommendations
        for idx, proj_rec in enumerate(project_recommendations[:2], 1):
            pr = ProjectRecommendation(
                analysis_id=analysis.id,
                project_name=proj_rec.get('title', ''),
                difficulty=proj_rec.get('difficulty', 'intermediate'),
                estimated_time=proj_rec.get('duration', ''),
                skills_learned=proj_rec.get('technologies', []),
                why_it_fits=proj_rec.get('why_recommended', ''),
                order=idx
            )
            db.add(pr)
        
        # Save experience analyses (simplified - can be enhanced)
        for exp_text in ResumeParser.extract_sections(resume_text).get("Experience", "").split("\n\n"):
            if exp_text.strip():
                ea = ExperienceAnalysis(
                    analysis_id=analysis.id,
                    experience_entry=exp_text.strip(),
                    match_score=exp_match * 100,
                    relevant_skills=matched_areas,
                    missing_skills=gaps,
                    assessment=exp_explanation
                )
                db.add(ea)
        
        db.commit()
        
        return {
            "analysisId": analysis.id,
            "status": "success",
            "atsScore": ats_score,
            "experienceMatch": exp_match * 100,
            "skillGapScore": skill_gap_score,
            "hiringRecommendation": recommendation
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/analysis/{analysisId}")
async def get_analysis(analysisId: int, db: Session = Depends(get_db)):
    """Get comprehensive analysis results"""
    
    analysis = db.query(AnalysisResult).filter(AnalysisResult.id == analysisId).first()
    
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")
    
    response = {
        "id": analysis.id,
        "atsScore": analysis.ats_score,
        "formatScore": analysis.format_score,
        "relevance": analysis.relevance_score,
        "experienceMatch": analysis.experience_match_score,
        "experienceMatchExplanation": analysis.experience_match_explanation,
        "skillGapScore": analysis.skill_gap_score,
        "summary": analysis.summary,
        "recruiterVerdict": analysis.recruiter_verdict,
        "hiringRecommendation": analysis.hiring_recommendation,
        "readinessLevel": analysis.readiness_level,
        "strengths": analysis.strengths or [],
        "weaknesses": analysis.weaknesses or [],
        "improvementPriorities": analysis.improvement_priorities or [],
        "inferredSkills": analysis.inferred_skills or [],
        "matchedKeywords": analysis.matched_keywords or [],
        "missingKeywords": analysis.missing_keywords or [],
        "matchedKeywordCount": analysis.matched_keyword_count,
        "missingKeywordCount": analysis.missing_keyword_count,
        "keywordMatches": [km.keyword for km in analysis.keyword_matches],
        "totalKeywords": len(analysis.keyword_matches),
        "presentSkills": [],
        "missingSkills": [ms.skill_name for ms in analysis.missing_skills],
        "recommendations": [
            {
                "title": r.title,
                "description": r.description,
                "action": r.action,
                "priority": r.priority,
                "category": r.category
            }
            for r in analysis.recommendations
        ],
        "experienceAnalyses": [
            {
                "experienceEntry": ea.experience_entry,
                "matchScore": ea.match_score,
                "relevantSkills": ea.relevant_skills or [],
                "missingSkills": ea.missing_skills or [],
                "assessment": ea.assessment
            }
            for ea in analysis.experience_analyses
        ],
        "projectAnalyses": [
            {
                "projectName": pa.project_name,
                "matchPercentage": pa.match_percentage,
                "relevantSkills": pa.relevant_skills or [],
                "missingSkills": pa.missing_skills or [],
                "improvementSuggestions": pa.improvement_suggestions or []
            }
            for pa in analysis.project_analyses
        ],
        "skillGaps": [
            {
                "skillName": sg.skill_name,
                "whyItMatters": sg.why_it_matters,
                "evidenceMissing": sg.evidence_missing,
                "recommendation": sg.recommendation,
                "priority": sg.priority
            }
            for sg in analysis.skill_gaps
        ],
        "projectRecommendations": [
            {
                "projectName": pr.project_name,
                "difficulty": pr.difficulty,
                "estimatedTime": pr.estimated_time,
                "skillsLearned": pr.skills_learned or [],
                "whyItFits": pr.why_it_fits,
                "order": pr.order
            }
            for pr in analysis.project_recommendations
        ],
        "resumeBullets": [
            {
                "skillGap": rb.skill_gap,
                "bulletPoint": rb.bullet_point,
                "section": rb.section
            }
            for rb in analysis.resume_bullets
        ],
        "improvedBullets": [
            {
                "originalText": ib.original_text,
                "improvedText": ib.improved_text,
                "impactMetric": ib.impact_metric,
                "type": ib.type
            }
            for ib in analysis.improved_bullets
        ],
        "createdAt": analysis.created_at.isoformat()
    }
    
    return response

@router.get("/analysis/{analysisId}/report")
async def download_report(analysisId: int, db: Session = Depends(get_db)):
    """Download analysis report as PDF"""
    
    analysis = db.query(AnalysisResult).filter(AnalysisResult.id == analysisId).first()
    
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")
    
    # TODO: Generate PDF report
    return {"message": "Report generation in progress"}
