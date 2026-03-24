from app.services import llm
import json

print("=" * 60)
print("Testing Role-Based Interview Mock Data")
print("=" * 60)

# Test Backend Role
print("\n" + "=" * 60)
print("TESTING: Backend Developer Role")
print("=" * 60)

backend_jd = "We are looking for a senior Backend Developer with experience in microservices architecture and REST APIs."

print("\n1. Testing Interview Questions (Backend Role):")
history = []
for turn in range(3):
    response = llm.generate_interview_followup(history, backend_jd, "")
    print(f"\nTurn {turn + 1}: {response}")
    history.append({"role": "assistant", "content": response})
    history.append({"role": "user", "content": f"Sample answer for turn {turn + 1}"})

print("\n2. Testing Interview Feedback (Backend Role):")
feedback = llm.generate_interview_feedback(history, backend_jd)
print(json.dumps(feedback, indent=2))

# Test UI/UX Role
print("\n\n" + "=" * 60)
print("TESTING: UI/UX Designer Role")
print("=" * 60)

uiux_jd = "We are seeking a talented UI/UX Designer to create beautiful and intuitive user interfaces for our web application."

print("\n1. Testing Interview Questions (UI/UX Role):")
history = []
for turn in range(3):
    response = llm.generate_interview_followup(history, uiux_jd, "")
    print(f"\nTurn {turn + 1}: {response}")
    history.append({"role": "assistant", "content": response})
    history.append({"role": "user", "content": f"Sample answer for turn {turn + 1}"})

print("\n2. Testing Interview Feedback (UI/UX Role):")
feedback = llm.generate_interview_feedback(history, uiux_jd)
print(json.dumps(feedback, indent=2))

print("\n" + "=" * 60)
print("Role-Based Interview Testing Complete!")
print("=" * 60)
