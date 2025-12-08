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

@router.get("/history", response_model=Any)
def get_user_history(
    db: Session = Depends(deps.get_db),
    current_user = Depends(deps.get_current_user)
) -> Any:
    """
    Get full history lists for all activities.
    """
    # 1. Assessments
    assessments_query = db.query(UserAssessmentAttempt).filter(UserAssessmentAttempt.user_id == current_user.id).order_by(UserAssessmentAttempt.timestamp.desc()).all()
    assessments_data = []
    for a in assessments_query:
        # Fetch related assessment title if possible (simple for now)
        assessments_data.append({
            "id": a.id,
            "type": "Assessment",
            "title": f"Daily Assessment {a.timestamp.date()}", 
            "score": f"{a.score}%" if a.score is not None else "N/A",
            "date": a.timestamp.strftime("%Y-%m-%d"),
            "status": "Completed"
        })

    # 2. Coding
    coding_query = db.query(CodingSubmission).filter(CodingSubmission.user_id == current_user.id).order_by(CodingSubmission.timestamp.desc()).all()
    coding_data = []
    for c in coding_query:
        coding_data.append({
            "id": c.id,
            "type": "Coding",
            "title": f"Coding Problem #{c.problem_id}", # Ideal: Join with Problem table
            "score": c.status,
            "date": c.timestamp.strftime("%Y-%m-%d"),
            "status": c.status
        })

    # 3. Interviews
    interviews_query = db.query(InterviewSession).filter(InterviewSession.user_id == current_user.id).order_by(InterviewSession.created_at.desc()).all()
    interview_data = []
    for i in interviews_query:
        interview_data.append({
            "id": i.id,
            "type": "Interview",
            "title": "Mock Interview Session",
            "score": f"{i.score}/100" if i.score else "Pending",
            "date": i.created_at.strftime("%Y-%m-%d"),
            "status": i.status
        })
    
    return {
        "assessments": assessments_data,
        "coding": coding_data,
        "interviews": interview_data
    }

@router.get("/history/assessment/{id}", response_model=Any)
def get_assessment_details(
    id: int,
    db: Session = Depends(deps.get_db),
    current_user = Depends(deps.get_current_user)
) -> Any:
    attempt = db.query(UserAssessmentAttempt).filter(UserAssessmentAttempt.id == id, UserAssessmentAttempt.user_id == current_user.id).first()
    if not attempt:
        return {"error": "Not found"}
    
    # Reconstruct details (In a real app, join with Questions)
    # For now, we return the stored responses
    return {
        "title": f"Daily Assessment {attempt.timestamp.date()}",
        "score": attempt.score,
        "date": attempt.timestamp.strftime("%Y-%m-%d"),
        "responses": attempt.responses # This contains the logical QA map
    }

@router.get("/history/coding/{id}", response_model=Any)
def get_coding_details(
    id: int,
    db: Session = Depends(deps.get_db),
    current_user = Depends(deps.get_current_user)
) -> Any:
    sub = db.query(CodingSubmission).filter(CodingSubmission.id == id, CodingSubmission.user_id == current_user.id).first()
    if not sub:
        return {"error": "Not found"}
        
    return {
        "title": f"Coding Problem #{sub.problem_id}",
        "status": sub.status,
        "date": sub.timestamp.strftime("%Y-%m-%d"),
        "language": sub.language,
        "code": sub.code
    }

@router.get("/history/interview/{id}", response_model=Any)
def get_interview_details(
    id: int,
    db: Session = Depends(deps.get_db),
    current_user = Depends(deps.get_current_user)
) -> Any:
    session = db.query(InterviewSession).filter(InterviewSession.id == id, InterviewSession.user_id == current_user.id).first()
    if not session:
        return {"error": "Not found"}
        
    # Get messages
    chat_history = []
    for m in session.messages:
        chat_history.append({"role": m.role, "content": m.content})
        
    return {
        "title": "Mock Interview Session",
        "date": session.created_at.strftime("%Y-%m-%d"),
        "score": session.score,
        "feedback": session.feedback,
        "transcript": chat_history,
        "job_description": session.job_description
    }
