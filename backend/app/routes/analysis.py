from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
import uuid
import os

from app.database import get_db
from app.models import (
    AnalysisResult,
    Resume,
    JobDescription,
    KeywordMatch,
    MissingSkill,
    Recommendation,
    ExperienceAnalysis,
    ProjectAnalysis,
    SkillGap,
    ProjectRecommendation,
    ResumeBullet,
)
from app.schemas import AnalysisResultResponse
from app.nlp_utils import ResumeParser, KeywordExtractor, ATSScorer
from app.gemini_engine import GeminiRecommendationEngine
from app.semantic_analyzer import SemanticAnalyzer
from app.config import settings

router = APIRouter()


@router.post("/analyze")
async def analyze_resume(
    resume: UploadFile = File(...),
    jobDescription: str = Form(...),
    db: Session = Depends(get_db),
):
    """Analyze resume against job description with intelligent recruiter-style evaluation"""

    try:
        # Read resume file
        resume_content = await resume.read()

        # Parse resume
        resume_text = ResumeParser.parse_resume(resume_content, resume.filename)

        # Extract keywords (legacy)
        matching_keywords, missing_keywords = KeywordExtractor.extract_keywords(
            resume_text, jobDescription
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
            len(required_skills),
        )

        # ============ NEW: Semantic Analysis ============
        semantic_analyzer = SemanticAnalyzer()

        # 1. Infer skills from projects, experience, certifications
        inferred_skills, skill_sources = semantic_analyzer.infer_skills_from_content(
            resume_text, jobDescription
        )

        # 2. Analyze experience
        experience_match, strengths, weaknesses, experience_assessment = (
            semantic_analyzer.analyze_experience(resume_text, jobDescription)
        )

        # 3. Analyze projects
        project_analyses = semantic_analyzer.analyze_projects(
            resume_text, jobDescription
        )

        # 4. Identify skill gaps
        skill_gaps = semantic_analyzer.identify_skill_gaps(resume_text, jobDescription)

        # 5. Generate resume bullets
        gap_names = [gap["skill"] for gap in skill_gaps]
        resume_bullets = semantic_analyzer.generate_resume_bullets(
            resume_text, gap_names
        )

        # 6. Recommend projects
        project_recommendations = semantic_analyzer.recommend_projects(
            resume_text, gap_names, jobDescription
        )

        # 7. Generate recruiter verdict
        hiring_recommendation, recruiter_verdict, improvement_priorities = (
            semantic_analyzer.generate_recruiter_verdict(
                experience_match, strengths, weaknesses, ats_score, skill_gaps
            )
        )

        # Generate legacy recommendations for backward compatibility
        recommendation_engine = GeminiRecommendationEngine()
        recommendations = recommendation_engine.generate_recommendations(
            resume_text, jobDescription, missing_skills, missing_keywords, ats_score
        )

        # ============ Save to Database ============

        job_desc_obj = JobDescription(title="Job Description", content=jobDescription)
        db.add(job_desc_obj)
        db.flush()

        resume_obj = Resume(
            user_id=1,  # TODO: Get from current user
            filename=resume.filename,
            file_path=f"uploads/{uuid.uuid4()}_{resume.filename}",
            original_text=resume_text,
        )
        db.add(resume_obj)
        db.flush()

        analysis = AnalysisResult(
            user_id=1,  # TODO: Get from current user
            resume_id=resume_obj.id,
            job_description_id=job_desc_obj.id,
            ats_score=ats_score,
            format_score=ATSScorer.evaluate_format(resume_text),
            relevance_score=len(matching_keywords)
            / max(1, len(matching_keywords) + len(missing_keywords))
            * 100,
            experience_match_score=experience_match * 100,
            summary=f"Your resume has an ATS score of {ats_score}%. You've matched {len(matching_keywords)} keywords out of {len(matching_keywords) + len(missing_keywords)}.",
            recruiter_verdict=recruiter_verdict,
            hiring_recommendation=hiring_recommendation,
            strengths=strengths,
            weaknesses=weaknesses,
            improvement_priorities=improvement_priorities,
            inferred_skills=inferred_skills,
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
                importance="high" if skill in missing_keywords else "medium",
            )
            db.add(ms)

        # Save recommendations (legacy)
        for rec in recommendations:
            r = Recommendation(
                analysis_id=analysis.id,
                title=rec.get("title", ""),
                description=rec.get("description", ""),
                action=rec.get("action", ""),
                priority=rec.get("priority", "medium"),
                category=rec.get("category", "general"),
            )
            db.add(r)

        # Save experience analyses
        for exp_text in (
            ResumeParser.extract_sections(resume_text)
            .get("Experience", "")
            .split("\n\n")
        ):
            if exp_text.strip():
                # Find matching analysis from semantic analyzer
                match_score = 50  # Default
                relevant = []
                missing = []
                assessment = "Experience relevant to role"

                ea = ExperienceAnalysis(
                    analysis_id=analysis.id,
                    experience_entry=exp_text.strip(),
                    match_score=match_score,
                    relevant_skills=relevant,
                    missing_skills=missing,
                    assessment=assessment,
                )
                db.add(ea)

        # Save project analyses
        for proj in project_analyses:
            pa = ProjectAnalysis(
                analysis_id=analysis.id,
                project_name=proj.get("name", ""),
                match_percentage=proj.get("match_percentage", 0),
                relevant_skills=proj.get("relevant_skills", []),
                missing_skills=proj.get("missing_skills", []),
                improvement_suggestions=proj.get("improvement_suggestions", []),
            )
            db.add(pa)

        # Save skill gaps
        for gap in skill_gaps:
            sg = SkillGap(
                analysis_id=analysis.id,
                skill_name=gap.get("skill", ""),
                why_it_matters=gap.get("why_it_matters", ""),
                evidence_missing=gap.get("evidence_missing", ""),
                recommendation=gap.get("recommendation", ""),
                priority=gap.get("priority", "medium"),
            )
            db.add(sg)

        # Save project recommendations
        for idx, proj_rec in enumerate(project_recommendations[:2], 1):
            pr = ProjectRecommendation(
                analysis_id=analysis.id,
                project_name=proj_rec.get("name", ""),
                difficulty=proj_rec.get("difficulty", "intermediate"),
                estimated_time=proj_rec.get("estimated_time", ""),
                skills_learned=proj_rec.get("skills_learned", []),
                why_it_fits=proj_rec.get("why_it_fits", ""),
                order=idx,
            )
            db.add(pr)

        # Save resume bullets
        for bullet in resume_bullets:
            rb = ResumeBullet(
                analysis_id=analysis.id,
                skill_gap=bullet.get("skill", ""),
                bullet_point=bullet.get("bullet", ""),
                section=bullet.get("section", "Experience"),
            )
            db.add(rb)

        db.commit()

        return {
            "analysisId": analysis.id,
            "status": "success",
            "atsScore": ats_score,
            "experienceMatch": experience_match * 100,
            "hiringRecommendation": hiring_recommendation,
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

    # Prepare response data
    response = {
        "id": analysis.id,
        "atsScore": analysis.ats_score,
        "formatScore": analysis.format_score,
        "relevance": analysis.relevance_score,
        "experienceMatch": analysis.experience_match_score,
        "summary": analysis.summary,
        "recruiterVerdict": analysis.recruiter_verdict,
        "hiringRecommendation": analysis.hiring_recommendation,
        "strengths": analysis.strengths or [],
        "weaknesses": analysis.weaknesses or [],
        "improvementPriorities": analysis.improvement_priorities or [],
        "inferredSkills": analysis.inferred_skills or [],
        "keywordMatches": [km.keyword for km in analysis.keyword_matches],
        "totalKeywords": len(analysis.keyword_matches),
        "presentSkills": [],
        "missingSkills": [ms.skill_name for ms in analysis.missing_skills],
        "missingKeywords": [ms.skill_name for ms in analysis.missing_skills],
        "recommendations": [
            {
                "title": r.title,
                "description": r.description,
                "action": r.action,
                "priority": r.priority,
                "category": r.category,
            }
            for r in analysis.recommendations
        ],
        "experienceAnalyses": [
            {
                "experienceEntry": ea.experience_entry,
                "matchScore": ea.match_score,
                "relevantSkills": ea.relevant_skills or [],
                "missingSkills": ea.missing_skills or [],
                "assessment": ea.assessment,
            }
            for ea in analysis.experience_analyses
        ],
        "projectAnalyses": [
            {
                "projectName": pa.project_name,
                "matchPercentage": pa.match_percentage,
                "relevantSkills": pa.relevant_skills or [],
                "missingSkills": pa.missing_skills or [],
                "improvementSuggestions": pa.improvement_suggestions or [],
            }
            for pa in analysis.project_analyses
        ],
        "skillGaps": [
            {
                "skillName": sg.skill_name,
                "whyItMatters": sg.why_it_matters,
                "evidenceMissing": sg.evidence_missing,
                "recommendation": sg.recommendation,
                "priority": sg.priority,
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
                "order": pr.order,
            }
            for pr in analysis.project_recommendations
        ],
        "resumeBullets": [
            {
                "skillGap": rb.skill_gap,
                "bulletPoint": rb.bullet_point,
                "section": rb.section,
            }
            for rb in analysis.resume_bullets
        ],
        "createdAt": analysis.created_at.isoformat(),
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
