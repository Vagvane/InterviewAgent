import sys
import os
from dotenv import load_dotenv
import json

sys.path.append(os.getcwd())
load_dotenv()

from app.services import llm

print("Testing Interview Generation...")

# Test Follow-up Question
print("\n1. Testing Follow-up Question Generation...")
history = [
    {"role": "assistant", "content": "Hello, I am your AI interviewer. Please introduce yourself."},
    {"role": "user", "content": "Hi, I am a Full Stack Developer with 3 years of experience in React and Python."}
]
jd = "Looking for a Full Stack Developer with experience in React, Node.js, and Python."
try:
    question = llm.generate_interview_followup(history, jd)
    print(f"Generated Question: {question}")
except Exception as e:
    print(f"FAILURE (Follow-up): {e}")

# Test Feedback Generation
print("\n2. Testing Feedback Generation...")
full_history = history + [
    {"role": "assistant", "content": "Great. Can you explain the difference between SQL and NoSQL?"},
    {"role": "user", "content": "SQL is relational, NoSQL is non-relational. SQL uses tables, NoSQL uses documents."}
]
try:
    feedback = llm.generate_interview_feedback(full_history, jd)
    print("Generated Feedback:")
    print(json.dumps(feedback, indent=2))
except Exception as e:
    print(f"FAILURE (Feedback): {e}")
