from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base_class import Base

class CodingProblem(Base):
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text, nullable=False)
    difficulty = Column(String) # Easy, Medium, Hard
    test_cases = Column(Text) # JSON string of test cases
    
class CodingSubmission(Base):
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    problem_id = Column(Integer, ForeignKey("codingproblem.id"))
    code = Column(Text, nullable=False)
    language = Column(String, default="python")
    status = Column(String) # Passed, Failed
    timestamp = Column(DateTime, default=datetime.utcnow)
