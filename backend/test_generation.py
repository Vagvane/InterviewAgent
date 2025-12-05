import sys
import os
from dotenv import load_dotenv

# Add current directory to path so we can import app
sys.path.append(os.getcwd())

load_dotenv()

from app.services import llm
import json

print("Testing Daily Question Generation...")
try:
    questions = llm.generate_daily_questions()
    print("\nSUCCESS! Generated questions:")
    print(json.dumps(questions[:2], indent=2)) # Print first 2
    print(f"... and {len(questions)-2} more.")
except Exception as e:
    print(f"\nFAILURE: {e}")
