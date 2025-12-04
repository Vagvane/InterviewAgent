from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base_class import Base

class InterviewSession(Base):
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    job_description = Column(Text, nullable=True)
    resume_text = Column(Text, nullable=True) # Extracted text from resume
    status = Column(String, default="active") # active, completed
    feedback = Column(JSON, nullable=True) # Store final report
    score = Column(Integer, nullable=True) # Overall interview score
    created_at = Column(DateTime, default=datetime.utcnow)
    messages = relationship("InterviewMessage", back_populates="session")

class InterviewMessage(Base):
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("interviewsession.id"))
    role = Column(String) # user, assistant
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    session = relationship("InterviewSession", back_populates="messages")
