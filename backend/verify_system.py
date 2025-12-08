import requests
import sys

API_URL = "http://localhost:8000/api/v1"

def print_result(name, success, message=""):
    if success:
        print(f"✅ {name}: PASSED")
    else:
        print(f"❌ {name}: FAILED - {message}")

def verify_system():
    print("🚀 Starting API Verification Check...")
    print("-------------------------------------")
    
    # 1. Login
    token = None
    try:
        # Try logging in with a test user or register one
        print("🔐 Testing Authentication...")
        email = "verify@example.com"
        password = "password123"
        
        # Try login first
        login_data = {"username": email, "password": password}
        res = requests.post(f"{API_URL}/login/access-token", data=login_data)
        
        if res.status_code == 401 or res.status_code == 400:
            # Register if not exists
            print("   User not found, registering...")
            reg_data = {"email": email, "password": password, "full_name": "Verification User"}
            requests.post(f"{API_URL}/users/", json=reg_data)
            # Login again
            res = requests.post(f"{API_URL}/login/access-token", data=login_data)
            
        if res.status_code == 200:
            token = res.json()["access_token"]
            print_result("Authentication", True)
        else:
            print_result("Authentication", False, f"Status {res.status_code}: {res.text}")
            return
            
    except Exception as e:
        print_result("Authentication", False, str(e))
        return

    headers = {"Authorization": f"Bearer {token}"}
    
    # 2. Assessment Generation (Daily)
    try:
        print("\n📝 Testing Assessment Generation (AI)...")
        # Force refresh to trigger AI
        res = requests.get(f"{API_URL}/assessment/daily?refresh=true", headers=headers)
        if res.status_code == 200:
            data = res.json()
            questions = data.get("questions", [])
            if len(questions) == 16: # 5+5+5+1
                print_result("Assessment Generation", True, f"Generated {len(questions)} questions")
            else:
                print_result("Assessment Generation", False, f"Expected 16 questions, got {len(questions)}")
        else:
            print_result("Assessment Generation", False, f"Status {res.status_code}: {res.text}")
    except Exception as e:
        print_result("Assessment Generation", False, str(e))

    # 3. Coding Problem Generation
    try:
        print("\n💻 Testing Coding Problem Generation (AI)...")
        res = requests.get(f"{API_URL}/coding/daily", headers=headers)
        if res.status_code == 200:
            data = res.json()
            if "title" in data and "test_cases" in data:
                 print_result("Coding Generation", True, f"Generated: {data['title']}")
            else:
                 print_result("Coding Generation", False, "Invalid response structure")
        else:
            print_result("Coding Generation", False, f"Status {res.status_code}: {res.text}")
    except Exception as e:
        print_result("Coding Generation", False, str(e))

    # 4. Interview Chat (With Session Start)
    try:
        print("\n🗣️ Testing Interview Chat (AI)...")
        # Start a new session first
        start_data = {
            "job_description": "Full Stack Developer role"
        }
        res_start = requests.post(f"{API_URL}/interview/start", data=start_data, headers=headers)
        if res_start.status_code == 200:
            session_id = res_start.json()["session_id"]
            print(f"   Session started with ID: {session_id}")
            
            # Send chat message
            chat_data = {"message": "Hello, I am ready for the interview."}
            res = requests.post(f"{API_URL}/interview/{session_id}/chat", json=chat_data, headers=headers)
            if res.status_code == 200:
                data = res.json()
                reply = data.get("response", "") or data.get("reply", "")
                if reply:
                    print_result("Interview Chat", True, f"AI Replied: {reply[:50]}...")
                else:
                     print_result("Interview Chat", False, "Empty reply")
            else:
                 print_result("Interview Chat", False, f"Chat Status {res.status_code}: {res.text}")
        else:
            print_result("Interview Chat", False, f"Start Status {res_start.status_code}: {res_start.text}")
            
    except Exception as e:
        print_result("Interview Chat", False, str(e))

    print("\n-------------------------------------")
    print("🏁 Verification Complete.")

if __name__ == "__main__":
    verify_system()
