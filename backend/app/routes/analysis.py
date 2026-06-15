from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from typing import Optional
from io import BytesIO
import uuid
import os
from pathlib import Path

from app.database import get_db
from app.models import (
    AnalysisResult, Resume, JobDescription, KeywordMatch, MissingSkill, Recommendation,
    ExperienceAnalysis, ProjectAnalysis, SkillGap, ProjectRecommendation, ResumeBullet, ImprovedBullet, User
)
from app.schemas import AnalysisResultResponse
from app.nlp_utils import ResumeParser, KeywordExtractor, ATSScorer
from app.gemini_engine import GeminiRecommendationEngine
from app.semantic_analyzer import SemanticAnalyzer
from app.config import settings
from app.routes.auth import get_current_user
from app.rate_limit import rate_limit
from app.upload_validation import validate_resume_upload

router = APIRouter()

@router.post(
    "/analyze",
    dependencies=[Depends(rate_limit(lambda: settings.ANALYSIS_RATE_LIMIT, "analysis"))],
)
async def analyze_resume(
    resume: UploadFile = File(...),
    jobDescription: str = Form(...),
    aiProcessingConsent: bool = Form(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Analyze resume against job description with intelligent recruiter-style evaluation"""
    
    try:
        if not aiProcessingConsent:
            raise HTTPException(
                status_code=400,
                detail="AI processing consent is required to analyze a resume.",
            )

        # Read resume file
        resume_content = await resume.read()
        validate_resume_upload(resume, resume_content)
        
        # Parse resume
        resume_text = ResumeParser.parse_resume(resume_content, resume.filename)
        
        # Extract keywords (legacy)
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
        
        # ============ NEW: Semantic Analysis ============
        semantic_analyzer = SemanticAnalyzer()
        ai_enabled = semantic_analyzer.model is not None
        analysis_data = semantic_analyzer.analyze_resume_complete(
        resume_text,
        jobDescription
        )
        # 0. Semantic keyword analysis + skill gap score
        matched_kw = analysis_data.get("matched_keywords", [])
        missing_kw = analysis_data.get("missing_keywords", [])

        matched_count = len(matched_kw)
        missing_count = len(missing_kw)

        skill_gap_score = semantic_analyzer.calculate_skill_gap_score(
            missing_count,
            matched_count
        )

        inferred_skills = analysis_data.get("inferred_skills", [])

        experience_match = analysis_data.get("experience_match", 0) / 100.0

        exp_explanation = analysis_data.get(
            "experience_explanation",
            ""
        )

        matched_areas = []
        exp_gaps = []

        strengths = analysis_data.get("strengths", [])
        weaknesses = analysis_data.get("weaknesses", [])
            
        # 3. Analyze projects
        project_analyses = []

        # 4. Identify skill gaps
        skill_gaps = []

        # 5. Generate resume bullets
        gap_names = []
        resume_bullets = []

        # 5b. Generate improved bullets
        improved_bullets_data = []

        # 6. Recommend projects
        project_recommendations = []
        
       # 7. Generate recruiter verdict

        hiring_recommendation = analysis_data.get(
            "hiring_recommendation",
            "Unavailable"
        )

        recruiter_verdict = analysis_data.get(
            "recruiter_verdict",
            "Unavailable"
        )

        readiness = analysis_data.get(
            "readiness_level",
            "Unavailable"
        )

        improvement_priorities = analysis_data.get(
            "recommendations",
            []
        )
        
       # Generate recommendations from master analysis

        recommendations = [
            {
                "title": "AI Recommendation",
                "description": rec,
                "action": rec,
                "priority": "medium",
                "category": "general"
            }
            for rec in analysis_data.get("recommendations", [])
        ]
        
        # ============ Save to Database ============
        
        job_desc_obj = JobDescription(
            title="Job Description",
            content=jobDescription
        )
        db.add(job_desc_obj)
        db.flush()
        
        safe_filename = Path(resume.filename or "resume").name
        resume_obj = Resume(
            user_id=current_user.id,
            filename=safe_filename,
            file_path=f"uploads/{uuid.uuid4()}_{safe_filename}",
            original_text=resume_text
        )
        db.add(resume_obj)
        db.flush()
        
        analysis = AnalysisResult(
            user_id=current_user.id,
            resume_id=resume_obj.id,
            job_description_id=job_desc_obj.id,
            ats_score=ats_score,
            format_score=ATSScorer.evaluate_format(resume_text),
            relevance_score=len(matching_keywords) / max(1, len(matching_keywords) + len(missing_keywords)) * 100,
            experience_match_score=experience_match * 100,
            experience_match_explanation=exp_explanation,
            summary=f"Your resume has an ATS score of {ats_score}%. You've matched {len(matching_keywords)} keywords out of {len(matching_keywords) + len(missing_keywords)}.",
            recruiter_verdict=recruiter_verdict,
            hiring_recommendation=hiring_recommendation,
            readiness_level=readiness,
            strengths=strengths,
            weaknesses=weaknesses,
            improvement_priorities=improvement_priorities,
            inferred_skills=inferred_skills,
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
        
        # Save experience analyses
        for exp_text in ResumeParser.extract_sections(resume_text).get("Experience", "").split("\n\n"):
            if exp_text.strip():
                ea = ExperienceAnalysis(
                    analysis_id=analysis.id,
                    experience_entry=exp_text.strip(),
                    match_score=experience_match * 100,
                    relevant_skills=matched_areas,
                    missing_skills=exp_gaps,
                    assessment=exp_explanation
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
                improvement_suggestions=proj.get("improvement_suggestions", [])
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
                priority=gap.get("priority", "medium")
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
                order=idx
            )
            db.add(pr)
        
        # Save resume bullets
        for bullet in resume_bullets:
            rb = ResumeBullet(
                analysis_id=analysis.id,
                skill_gap=bullet.get("skill", ""),
                bullet_point=bullet.get("bullet", ""),
                section=bullet.get("section", "Experience")
            )
            db.add(rb)

        # Save improved bullets
        for bullet in improved_bullets_data:
            ib = ImprovedBullet(
                analysis_id=analysis.id,
                original_text=bullet.get("original", ""),
                improved_text=bullet.get("improved", ""),
                impact_metric=bullet.get("metric"),
                type=bullet.get("type", "achievement")
            )
            db.add(ib)
        
        db.commit()
        
        return {
            "analysisId": analysis.id,
            "status": "success",
            "atsScore": ats_score,
            "experienceMatch": experience_match * 100,
            "hiringRecommendation": hiring_recommendation,
            "aiEnabled": ai_enabled
        }
        
    except HTTPException:
        db.rollback()
        raise
    except Exception:
        db.rollback()
        raise HTTPException(status_code=400, detail="Resume analysis failed. Please try again.")

@router.get("/analysis/{analysisId}")
async def get_analysis(analysisId: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Get comprehensive analysis results"""
    
    analysis = db.query(AnalysisResult).filter(
        AnalysisResult.id == analysisId,
        AnalysisResult.user_id == current_user.id,
        AnalysisResult.deleted_at.is_(None)
    ).first()
    
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")
    
    # Prepare response data
    response = {
        "id": analysis.id,
        "atsScore": analysis.ats_score,
        "formatScore": analysis.format_score,
        "relevance": analysis.relevance_score,
        "experienceMatch": analysis.experience_match_score,
        "experienceMatchExplanation": analysis.experience_match_explanation,
        "skillGapScore": analysis.skill_gap_score or 0.0,
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
        "matchedKeywordCount": analysis.matched_keyword_count or 0,
        "missingKeywordCount": analysis.missing_keyword_count or 0,
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
        "createdAt": analysis.created_at.isoformat(),
        "aiEnabled": bool(analysis.skill_gaps or analysis.experience_analyses or analysis.inferred_skills)
    }
    
    return response

@router.get("/analysis/{analysisId}/report")
async def download_report(analysisId: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Download analysis report as PDF"""
    
    analysis = db.query(AnalysisResult).filter(
        AnalysisResult.id == analysisId,
        AnalysisResult.user_id == current_user.id,
        AnalysisResult.deleted_at.is_(None)
    ).first()
    
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")

    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import cm
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
    from reportlab.lib import colors

    buf = BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4,
                            leftMargin=2*cm, rightMargin=2*cm,
                            topMargin=2*cm, bottomMargin=2*cm)
    styles = getSampleStyleSheet()
    h1 = styles["h1"]
    h2 = ParagraphStyle("h2", parent=styles["Heading2"], spaceAfter=4)
    body = styles["Normal"]
    bullet_style = ParagraphStyle("bullet", parent=body, leftIndent=12, spaceAfter=2)

    def section(title):
        return [Spacer(1, 10), Paragraph(title, h2),
                HRFlowable(width="100%", thickness=0.5, color=colors.grey)]

    def bullets(items):
        return [Paragraph(f"• {item}", bullet_style) for item in (items or [])]

    score_color = "green" if analysis.ats_score >= 70 else ("orange" if analysis.ats_score >= 50 else "red")
    created = analysis.created_at.strftime("%B %d, %Y")
    filename = analysis.resume.filename if analysis.resume else "Resume"

    story = [
        Paragraph("Resume Analysis Report", h1),
        Paragraph(f"<font color='grey'>Generated {created} &nbsp;|&nbsp; {filename}</font>", body),
        Spacer(1, 14),

        *section("ATS Score"),
        Paragraph(f"<font color='{score_color}' size='18'><b>{analysis.ats_score:.1f}%</b></font>", body),
        Paragraph(f"Format Score: {analysis.format_score:.1f}% &nbsp;|&nbsp; Experience Match: {analysis.experience_match_score:.1f}%", body),

        *section("Hiring Recommendation"),
        Paragraph(f"<b>{analysis.hiring_recommendation or 'N/A'}</b>", body),
        Spacer(1, 6),
        Paragraph(analysis.recruiter_verdict or "No verdict available.", body),

        *section("Strengths"),
        *bullets(analysis.strengths),

        *section("Weaknesses"),
        *bullets(analysis.weaknesses),

        *section("Improvement Priorities"),
        *bullets(analysis.improvement_priorities),

        *section("Skill Gaps"),
        *[Paragraph(f"• <b>{sg.skill_name}</b> [{sg.priority}] — {sg.why_it_matters}", bullet_style)
          for sg in analysis.skill_gaps],

        *section("Missing Skills"),
        *[Paragraph(f"• {ms.skill_name} ({ms.importance})", bullet_style)
          for ms in analysis.missing_skills],

        *section("Recommendations"),
        *[Paragraph(f"• <b>{r.title}</b>: {r.description}", bullet_style)
          for r in analysis.recommendations],
    ]

    doc.build(story)
    buf.seek(0)
    return StreamingResponse(
        buf,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename=analysis-{analysisId}.pdf"}
    )
