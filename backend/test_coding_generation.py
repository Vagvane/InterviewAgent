import sys
import os
from dotenv import load_dotenv
import json

sys.path.append(os.getcwd())
load_dotenv()

from app.services import llm

print("Testing Coding Problem Generation...")
try:
    problem = llm.generate_coding_problem()
    print("\nGenerated Problem:")
    print(json.dumps(problem, indent=2))
except Exception as e:
    print(f"\nFAILURE: {e}")
