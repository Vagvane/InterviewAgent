from typing import Any
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, Body
from sqlalchemy.orm import Session
from app.api import deps
from app.models.interview import InterviewSession, InterviewMessage
from app.services import llm

router = APIRouter()

@router.post("/start", response_model=Any)
def start_interview(
    job_description: str = Form(...),
    resume: UploadFile = File(None),
    db: Session = Depends(deps.get_db),
    current_user = Depends(deps.get_current_user)
) -> Any:
    """
    Start a new interview session with JD and optional Resume.
    """
    resume_text = ""
    if resume:
        # Mock resume parsing
        resume_text = "Parsed resume content..."
    
    session = InterviewSession(
        user_id=current_user.id,
        job_description=job_description,
        resume_text=resume_text
    )
    db.add(session)
    db.commit()
    db.refresh(session)
    return {"session_id": session.id, "message": "Interview started. Please introduce yourself."}

@router.post("/{session_id}/chat", response_model=Any)
def chat_interview(
    session_id: int,
    message: Any = Body(...), # Expect JSON: { "message": "..." }
    db: Session = Depends(deps.get_db),
    current_user = Depends(deps.get_current_user)
) -> Any:
    """
    Send a message to the interviewer avatar.
    """
    user_content = message.get("message")
    session = db.query(InterviewSession).filter(InterviewSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    # Save user message
    user_msg = InterviewMessage(session_id=session.id, role="user", content=user_content)
    db.add(user_msg)
    
    # Fetch recent history for context (last 20 messages for better context)
    history_msgs = db.query(InterviewMessage).filter(InterviewMessage.session_id == session.id).order_by(InterviewMessage.timestamp.asc()).limit(20).all()
    history = [{"role": msg.role, "content": msg.content} for msg in history_msgs]
    
    # Generate AI response using LLM with staged logic
    ai_response_text = llm.generate_interview_followup(history, session.job_description, session.resume_text or "")
    
    ai_msg = InterviewMessage(session_id=session.id, role="assistant", content=ai_response_text)
    db.add(ai_msg)
    
    db.commit()
    return {"response": ai_response_text, "audio_url": "mock_audio_url.mp3"}

@router.post("/{session_id}/end", response_model=Any)
def end_interview(
    session_id: int,
    db: Session = Depends(deps.get_db),
    current_user = Depends(deps.get_current_user)
) -> Any:
    """
    End the interview session and generate feedback.
    """
    session = db.query(InterviewSession).filter(InterviewSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    session.status = "completed"
    
    # Fetch full history for feedback generation
    history_msgs = db.query(InterviewMessage).filter(InterviewMessage.session_id == session.id).order_by(InterviewMessage.timestamp.asc()).all()
    history = [{"role": msg.role, "content": msg.content} for msg in history_msgs]
    
    # Generate Feedback
    feedback = llm.generate_interview_feedback(history, session.job_description)
    
    session.feedback = feedback
    session.score = feedback.get("score", 0)
    
    db.commit()
    
    return {"message": "Interview ended successfully.", "feedback": feedback}
