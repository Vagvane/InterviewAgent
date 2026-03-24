from app.services import llm
import json

print("=" * 50)
print("Testing Mock Assessment Questions")
print("=" * 50)
questions = llm.generate_daily_questions()
print(f"Generated {len(questions)} assessment questions")
print("\nAssessment Question Sample:")
print(json.dumps(questions[0], indent=2))

print("\n" + "=" * 50)
print("Testing Mock Coding Problems")
print("=" * 50)
problem = llm.generate_coding_problem()
print(f"Generated problem: {problem['title']}")
print(f"Difficulty: {problem['difficulty']}")
print(f"Test Cases: {len(problem['test_cases'])}")
print("\nCoding Problem Details:")
print(json.dumps(problem, indent=2))
