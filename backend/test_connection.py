import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
base_url = os.getenv("OPENAI_API_BASE")
model = os.getenv("OPENAI_MODEL_NAME", "gpt-3.5-turbo")

print(f"Testing Connection...")
print(f"API Key: {api_key[:5]}...{api_key[-5:] if api_key else 'None'}")
print(f"Base URL: {base_url}")
print(f"Model: {model}")

if not api_key or "INSERT_YOUR" in api_key:
    print("ERROR: Invalid API Key. Please update .env file.")
    exit(1)

try:
    client = OpenAI(
        api_key=api_key,
        base_url=base_url
    )

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "user", "content": "Hello, are you working?"}
        ]
    )
    
    print("\nSUCCESS! Connection established.")
    print(f"Response: {response.choices[0].message.content}")

except Exception as e:
    print(f"\nFAILURE: Connection failed.")
    print(f"Error: {e}")
