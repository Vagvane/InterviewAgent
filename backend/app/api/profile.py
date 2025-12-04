from typing import Any
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api import deps
from app.models.assessment import UserAssessmentAttempt
from app.models.coding import CodingSubmission
from app.models.interview import InterviewSession

router = APIRouter()

@router.get("/stats", response_model=Any)
def get_user_stats(
    db: Session = Depends(deps.get_db),
    current_user = Depends(deps.get_current_user)
) -> Any:
    """
    Get aggregated user statistics.
    """
    # Assessment Stats
    assessments = db.query(UserAssessmentAttempt).filter(UserAssessmentAttempt.user_id == current_user.id).all()
    total_assessments = len(assessments)
    avg_score = sum([a.score for a in assessments if a.score]) / total_assessments if total_assessments > 0 else 0
    
    # Coding Stats
    coding_subs = db.query(CodingSubmission).filter(CodingSubmission.user_id == current_user.id).all()
    total_coding = len(coding_subs)
    passed_coding = len([c for c in coding_subs if c.status == "Passed"])
    
    # Interview Stats
    interviews = db.query(InterviewSession).filter(InterviewSession.user_id == current_user.id).all()
    total_interviews = len(interviews)
    
    total_completed = total_assessments + passed_coding

    # Dynamic Skills Analysis
    skills = {
        "Python": "Beginner",
        "Problem Solving": "Beginner",
        "Communication": "Beginner"
    }

    # 1. Python Skill: Based on passed coding submissions
    if passed_coding > 5:
        skills["Python"] = "Advanced"
    elif passed_coding > 2:
        skills["Python"] = "Intermediate"
    
    # 2. Problem Solving: Based on Assessment Average
    if avg_score > 80:
        skills["Problem Solving"] = "Advanced"
    elif avg_score > 50:
        skills["Problem Solving"] = "Intermediate"

    # 3. Communication: Based on Interview Feedback (Mock logic for now as feedback is complex JSON)
    # In a real app, we would parse the 'strengths' list from the latest interview
    if total_interviews > 0:
        last_interview = interviews[-1]
        if last_interview.score and last_interview.score > 80:
            skills["Communication"] = "Advanced"
        elif last_interview.score and last_interview.score > 60:
            skills["Communication"] = "Intermediate"

    return {
        "assessments": {
            "total": total_assessments,
            "average_score": avg_score
        },
        "coding": {
            "total_submissions": total_coding,
            "passed": passed_coding
        },
        "interviews": {
            "total": total_interviews
        },
        "total_completed": total_completed,
        "skills_analysis": skills
    }
