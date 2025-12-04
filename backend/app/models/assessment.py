from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, JSON, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base_class import Base

class Assessment(Base):
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    date = Column(DateTime, default=datetime.utcnow)
    questions = relationship("Question", back_populates="assessment")

class Question(Base):
    id = Column(Integer, primary_key=True, index=True)
    assessment_id = Column(Integer, ForeignKey("assessment.id"))
    text = Column(Text, nullable=False)
    type = Column(String) # "mcq" or "subjective"
    category = Column(String, default="General") # Java, DSA, OOP, etc.
    options = Column(JSON, nullable=True) # For MCQ: ["A", "B", "C", "D"]
    correct_answer = Column(Text, nullable=True) # For auto-grading MCQ
    assessment = relationship("Assessment", back_populates="questions")

class UserAssessmentAttempt(Base):
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    assessment_id = Column(Integer, ForeignKey("assessment.id"))
    score = Column(Integer, nullable=True)
    responses = Column(JSON) # Store user answers
    timestamp = Column(DateTime, default=datetime.utcnow)
