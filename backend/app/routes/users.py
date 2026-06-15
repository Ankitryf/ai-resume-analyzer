from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import AnalysisResult, JobDescription, Resume, User
from app.routes.auth import get_current_user
from app.schemas import UserResponse

router = APIRouter()


@router.get("/me", response_model=UserResponse)
async def read_current_user(current_user: User = Depends(get_current_user)):
    return current_user


@router.get("/me/analyses")
async def get_current_user_analyses(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    analyses = (
        db.query(AnalysisResult)
        .filter(
            AnalysisResult.user_id == current_user.id,
            AnalysisResult.deleted_at.is_(None),
        )
        .order_by(AnalysisResult.created_at.desc())
        .all()
    )

    return [
        {
            "id": analysis.id,
            "atsScore": analysis.ats_score,
            "createdAt": analysis.created_at.isoformat(),
            "resumeFilename": analysis.resume.filename if analysis.resume else None,
        }
        for analysis in analyses
    ]


@router.get("/me/export")
async def export_current_user_data(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    analyses = (
        db.query(AnalysisResult)
        .filter(
            AnalysisResult.user_id == current_user.id,
            AnalysisResult.deleted_at.is_(None),
        )
        .order_by(AnalysisResult.created_at.desc())
        .all()
    )

    return {
        "user": {
            "id": current_user.id,
            "email": current_user.email,
            "username": current_user.username,
            "fullName": current_user.full_name,
            "createdAt": current_user.created_at.isoformat(),
        },
        "analyses": [
            {
                "id": analysis.id,
                "atsScore": analysis.ats_score,
                "formatScore": analysis.format_score,
                "relevanceScore": analysis.relevance_score,
                "summary": analysis.summary,
                "hiringRecommendation": analysis.hiring_recommendation,
                "readinessLevel": analysis.readiness_level,
                "matchedKeywords": analysis.matched_keywords or [],
                "missingKeywords": analysis.missing_keywords or [],
                "createdAt": analysis.created_at.isoformat(),
                "resume": {
                    "id": analysis.resume.id,
                    "filename": analysis.resume.filename,
                    "originalText": analysis.resume.original_text,
                }
                if analysis.resume
                else None,
                "jobDescription": {
                    "id": analysis.job_description.id,
                    "title": analysis.job_description.title,
                    "content": analysis.job_description.content,
                }
                if analysis.job_description
                else None,
            }
            for analysis in analyses
        ],
    }


@router.delete("/me/analyses/{analysis_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_current_user_analysis(
    analysis_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    analysis = (
        db.query(AnalysisResult)
        .filter(
            AnalysisResult.id == analysis_id,
            AnalysisResult.user_id == current_user.id,
            AnalysisResult.deleted_at.is_(None),
        )
        .first()
    )

    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")

    now = datetime.utcnow()
    analysis.deleted_at = now

    if analysis.resume:
        analysis.resume.deleted_at = now
    if analysis.job_description:
        analysis.job_description.deleted_at = now

    db.commit()
    return None


@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
async def delete_current_user_account(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    now = datetime.utcnow()

    current_user.is_active = False
    current_user.deleted_at = now

    db.query(Resume).filter(
        Resume.user_id == current_user.id,
        Resume.deleted_at.is_(None),
    ).update({"deleted_at": now}, synchronize_session=False)

    analyses = (
        db.query(AnalysisResult)
        .filter(
            AnalysisResult.user_id == current_user.id,
            AnalysisResult.deleted_at.is_(None),
        )
        .all()
    )
    for analysis in analyses:
        analysis.deleted_at = now
        if analysis.job_description:
            analysis.job_description.deleted_at = now

    db.commit()
    return None


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    current_user: User = Depends(get_current_user),
):
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to access this user")
    return current_user


@router.get("/{user_id}/analyses")
async def get_user_analyses(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to access these analyses")
    return await get_current_user_analyses(db=db, current_user=current_user)

