from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from app.api import deps
from app.models.assessment import Assessment, Question, UserAssessmentAttempt
from app.services import llm
from datetime import datetime

router = APIRouter()

@router.get("/daily", response_model=Any)
def get_daily_assessment(
    refresh: bool = False,
    db: Session = Depends(deps.get_db),
    current_user = Depends(deps.get_current_user)
) -> Any:
    """
    Get or generate daily assessment.
    """
    today = datetime.utcnow().date()
    
    # Check for existing assessment created today
    existing_assessment = db.query(Assessment).filter(
        Assessment.date >= datetime.combine(today, datetime.min.time()),
        Assessment.date < datetime.combine(today, datetime.max.time())
    ).first()
    
    if existing_assessment and not refresh:
        # Check if any question has "General" category (which we want to avoid)
        has_general = any((q.category == "General" or q.category is None) for q in existing_assessment.questions)
        
        if not has_general:
            # Return questions from DB
            return {"questions": [
                {
                    "id": q.id,
                    "text": q.text,
                    "type": q.type,
                    "options": q.options,
                    "category": q.category if hasattr(q, "category") else "General"
                } for q in existing_assessment.questions
            ]}
        # If has_general is True, we fall through to generate new questions (Auto-heal)

    # Generate new questions
    questions_data = llm.generate_daily_questions()
    
    # Save to DB
    new_assessment = Assessment(title=f"Daily Assessment {today}", date=datetime.utcnow())
    db.add(new_assessment)
    db.commit()
    db.refresh(new_assessment)
    
    for q_data in questions_data:
        q = Question(
            assessment_id=new_assessment.id,
            text=q_data["text"],
            type=q_data["type"],
            options=q_data.get("options"),
            correct_answer=q_data.get("correct_answer"),
            category=q_data.get("category", "General")
        )
        db.add(q)
    
    db.commit()
    
    return {"questions": questions_data}

@router.post("/submit", response_model=Any)
def submit_assessment(
    responses: Any = Body(...),
    db: Session = Depends(deps.get_db),
    current_user = Depends(deps.get_current_user)
) -> Any:
    """
    Submit assessment responses.
    """
    # Calculate score logic
    today = datetime.utcnow().date()
    
    # Fetch today's assessment to get correct answers
    assessment = db.query(Assessment).filter(
        Assessment.date >= datetime.combine(today, datetime.min.time()),
        Assessment.date < datetime.combine(today, datetime.max.time())
    ).first()
    
    correct_count = 0
    total_questions = 0
    
    if assessment:
        user_responses = responses.get("responses", {})
        for q in assessment.questions:
            if q.type == "mcq":
                total_questions += 1
                # Match by question text
                user_answer = user_responses.get(q.text)
                if user_answer == q.correct_answer:
                    correct_count += 1
    else:
        # Fallback if no assessment found in DB (shouldn't happen normally)
        # We could try to score against MOCK_QUESTIONS as a backup
        from app.services.llm import MOCK_QUESTIONS
        for q in MOCK_QUESTIONS:
            if q["type"] == "mcq":
                total_questions += 1
                if responses.get("responses", {}).get(q["text"]) == q["correct_answer"]:
                    correct_count += 1

    # Calculate percentage
    if total_questions > 0:
        score = int((correct_count / total_questions) * 100)
    else:
        score = 0
    
    # Save attempt
    attempt = UserAssessmentAttempt(
        user_id=current_user.id,
        assessment_id=None, # We don't have real assessment IDs yet in this mock flow
        score=score,
        responses=responses.get("responses"),
        timestamp=datetime.utcnow()
    )
    db.add(attempt)
    db.commit()
    db.refresh(attempt)
    
    return {
        "status": "submitted", 
        "score": score,
        "results": [
            {
                "question": q.text,
                "user_answer": user_responses.get(q.text),
                "correct_answer": q.correct_answer,
                "is_correct": user_responses.get(q.text) == q.correct_answer,
                "category": q.category
            } for q in assessment.questions if q.type == "mcq"
        ]
    }
