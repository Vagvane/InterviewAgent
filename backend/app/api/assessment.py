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
        # Check if any question has "General" category or is missing correct_answer
        has_general = any((q.category == "General" or q.category is None) for q in existing_assessment.questions)
        has_missing_answer = any((q.correct_answer is None) for q in existing_assessment.questions if q.type == "mcq")
        
        if not has_general and not has_missing_answer:
            # Return questions from DB with all fields including correct_answer
            return {"questions": [
                {
                    "id": q.id,
                    "text": q.text,
                    "type": q.type,
                    "options": q.options,
                    "correct_answer": q.correct_answer or "",
                    "category": q.category if hasattr(q, "category") else "General"
                } for q in existing_assessment.questions
            ]}
        # If has_general or missing_answer is True, we fall through to generate new questions (Auto-heal)

    # Generate new questions
    try:
        questions_data = llm.generate_daily_questions()
        print(f"Generated {len(questions_data)} assessment questions")
    except Exception as e:
        print(f"Assessment generation failed: {str(e)}")
        raise HTTPException(status_code=503, detail=f"Assessment generation failed: {str(e)}")
    
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
            correct_answer=q_data.get("correct_answer", ""),
            category=q_data.get("category", "General")
        )
        db.add(q)
    
    db.commit()
    
    # Return questions with correct_answer included for frontend to display on submission
    return {"questions": [
        {
            "id": q.id,
            "text": q.text,
            "type": q.type,
            "options": q.options,
            "correct_answer": q.correct_answer or q_data.get("correct_answer", ""),
            "category": q.category
        } for q, q_data in zip(db.query(Question).filter(Question.assessment_id == new_assessment.id).all(), questions_data)
    ]}

@router.post("/submit", response_model=Any)
def submit_assessment(
    responses: Any = Body(...),
    db: Session = Depends(deps.get_db),
    current_user = Depends(deps.get_current_user)
) -> Any:
    """
    Submit assessment responses and get detailed feedback.
    Shows correct answers even when user answers are wrong (for all mock and real questions).
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
    detailed_results = []
    
    if assessment:
        user_responses = responses.get("responses", {})
        questions = db.query(Question).filter(Question.assessment_id == assessment.id).all()
        
        for q in questions:
            if q.type == "mcq":
                total_questions += 1
                # Match by question text
                user_answer = user_responses.get(q.text)
                is_correct = user_answer == q.correct_answer
                
                if is_correct:
                    correct_count += 1
                
                # Build detailed result for each question
                result = {
                    "question": q.text,
                    "user_answer": user_answer,
                    "correct_answer": q.correct_answer or "",
                    "is_correct": is_correct,
                    "category": q.category,
                    "explanation": ""  # Can be enhanced with more context
                }
                
                # Add explanation for wrong answers
                if not is_correct and user_answer:
                    result["explanation"] = f"You selected: '{user_answer}'. The correct answer is: '{q.correct_answer}'"
                elif not is_correct and not user_answer:
                    result["explanation"] = f"You didn't select an answer. The correct answer is: '{q.correct_answer}'"
                elif is_correct:
                    result["explanation"] = "Correct! Well done."
                
                detailed_results.append(result)
            
            elif q.type == "subjective":
                # For subjective answers, show the model answer for comparison
                user_answer = user_responses.get(q.text)
                detailed_results.append({
                    "question": q.text,
                    "user_answer": user_answer,
                    "model_answer": q.correct_answer or "",
                    "category": q.category,
                    "type": "subjective",
                    "note": "Please compare your answer with the model answer provided below."
                })
    else:
        raise HTTPException(status_code=404, detail="No active assessment found to submit against.")

    # Calculate percentage
    if total_questions > 0:
        score = int((correct_count / total_questions) * 100)
    else:
        score = 0
    
    # Save attempt
    attempt = UserAssessmentAttempt(
        user_id=current_user.id,
        assessment_id=assessment.id if assessment else None,
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
        "correct_count": correct_count,
        "total_count": total_questions,
        "results": detailed_results
    }
