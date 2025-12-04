import os
import sys
from dotenv import load_dotenv

# Load env directly to be sure
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
print(f"API Key loaded: {api_key[:8]}...{api_key[-4:] if api_key else 'None'}")

try:
    import openai
    print(f"OpenAI Version: {openai.__version__}")
except ImportError:
    print("OpenAI library not installed.")
    sys.exit(1)

try:
    from openai import OpenAI
    client = OpenAI(api_key=api_key)
    print("Client initialized. Attempting request...")
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Hello"}]
    )
    print("Success!")
    print(response.choices[0].message.content)
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
