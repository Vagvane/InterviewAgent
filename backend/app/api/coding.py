from typing import Any
from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from app.api import deps
from app.models.coding import CodingProblem, CodingSubmission
from app.services import llm

router = APIRouter()

@router.get("/daily", response_model=Any)
def get_daily_coding_problem(
    refresh: bool = False,
    db: Session = Depends(deps.get_db),
    current_user = Depends(deps.get_current_user)
) -> Any:
    """
    Get daily coding problem.
    """
    # For now, we won't persist the daily problem to DB to allow easy "Next Question"
    # In a real app, we'd save it. Here we just generate on fly if refresh=True
    # or return a cached one if we had a cache. 
    # Since the user wants "Load Next Question", we'll just generate every time for now 
    # or rely on frontend to ask for it.
    
    return llm.generate_coding_problem()

@router.post("/run", response_model=Any)
def run_code(
    payload: Any = Body(...),
    db: Session = Depends(deps.get_db),
    current_user = Depends(deps.get_current_user)
) -> Any:
    """
    Run code against test cases.
    """
    code = payload.get("code")
    language = payload.get("language")
    
    # Use LLM to evaluate code
    result = llm.evaluate_code(code, language, "Two Sum")
    
    return {
        "status": "success", 
        "output": result.get("output", "Execution finished."),
        "analysis": result.get("analysis")
    }

@router.post("/submit", response_model=Any)
def submit_code(
    payload: Any = Body(...),
    db: Session = Depends(deps.get_db),
    current_user = Depends(deps.get_current_user)
) -> Any:
    """
    Submit code solution.
    """
    code = payload.get("code")
    language = payload.get("language")
    problem_id = payload.get("problem_id", 1) # Default to 1 for now
    
    # Use LLM to evaluate code
    result = llm.evaluate_code(code, language, "Two Sum")
    
    status = "Failed"
    if result.get("status") == "success":
        status = "Passed"
        
    # Save submission
    submission = CodingSubmission(
        user_id=current_user.id,
        problem_id=problem_id,
        code=code,
        language=language,
        status=status,
        timestamp=datetime.utcnow()
    )
    db.add(submission)
    db.commit()
    db.refresh(submission)
    
    return {
        "status": "submitted", 
        "result": result.get("output", "Submission processed."), 
        "analysis": result.get("analysis"),
        "submission_id": submission.id
    }
