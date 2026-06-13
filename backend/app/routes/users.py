from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User
from app.schemas import UserResponse

router = APIRouter()


@router.get("/me", response_model=UserResponse)
async def get_current_user(user_id: int = 1, db: Session = Depends(get_db)):
    """Get current user profile"""

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    """Get user profile by ID"""

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


@router.get("/{user_id}/analyses")
async def get_user_analyses(user_id: int, db: Session = Depends(get_db)):
    """Get all analyses for a user"""

    from app.models import AnalysisResult

    analyses = db.query(AnalysisResult).filter(AnalysisResult.user_id == user_id).all()

    return [
        {
            "id": a.id,
            "atsScore": a.ats_score,
            "createdAt": a.created_at.isoformat(),
            "resumeFilename": a.resume.filename if a.resume else None,
        }
        for a in analyses
    ]
