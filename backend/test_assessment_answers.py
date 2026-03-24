import sys
sys.path.insert(0, '.')
from app.services import llm
import json

print("=" * 60)
print("TESTING MOCK ASSESSMENT WITH CORRECT ANSWERS")
print("=" * 60)

# Test mock assessment generation
questions = llm.generate_daily_questions()
print(f'\nGenerated {len(questions)} questions')

print("\n--- First Question Details ---")
q = questions[0]
print(f'Text: {q["text"]}')
print(f'Type: {q["type"]}')
print(f'Options: {q["options"]}')
print(f'Correct Answer: {q["correct_answer"]}')
print(f'Category: {q["category"]}')

print("\n--- All Questions Summary ---")
for i, q in enumerate(questions):
    print(f"{i+1}. {q['category']} - {q['type']}")
    print(f"   Question: {q['text'][:60]}...")
    print(f"   Correct Answer: {q['correct_answer']}")

print("\n✓ All mock questions have correct_answer field!")
