import requests
import json

# We need to bypass auth for this test or use a valid token.
# Since we can't easily get a token without login flow, we'll temporarily disable auth in the endpoint
# OR we can just rely on the fact that we fixed the generation and assume run works if LLM works.
# But the user asked to ensure run/submit works.

# Let's try to hit the endpoint. If it returns 401, we know the endpoint is reachable.
# To properly test, we should mock the user or use the same trick as before (disable auth temporarily).
# However, modifying code just for testing is risky.

# Let's check if we can generate a token.
# Actually, the user's issue was "application is still not loading".
# If generation works, the app should load.
# The "Run" and "Submit" are separate actions.

# Let's create a script that just calls the LLM evaluation function directly to verify it works,
# bypassing the API layer which requires auth. This verifies the LOGIC.

import sys
import os
from dotenv import load_dotenv

sys.path.append(os.getcwd())
load_dotenv()

from app.services import llm

print("Testing Code Evaluation...")
code = """
def solution(nums, target):
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return []
"""
language = "python"
problem_title = "Two Sum"

try:
    result = llm.evaluate_code(code, language, problem_title)
    print("\nEvaluation Result:")
    print(json.dumps(result, indent=2))
except Exception as e:
    print(f"\nFAILURE: {e}")
