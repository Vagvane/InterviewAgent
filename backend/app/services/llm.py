import openai
from app.core.config import settings
import json
import random

# Extended Mock response to meet new requirements
MOCK_QUESTIONS = [
    # 5 Java Questions
    {"category": "Java", "type": "mcq", "text": "Which of these is not a Java feature?", "options": ["Object-oriented", "Use of pointers", "Portable", "Dynamic"], "correct_answer": "Use of pointers"},
    {"category": "Java", "type": "mcq", "text": "What is the return type of the hashCode() method in the Object class?", "options": ["Object", "int", "long", "void"], "correct_answer": "int"},
    {"category": "Java", "type": "mcq", "text": "Which exception is thrown when a divide by zero occurs?", "options": ["ArithmeticException", "NullPointerException", "ClassCastException", "IndexOutOfBoundsException"], "correct_answer": "ArithmeticException"},
    {"category": "Java", "type": "mcq", "text": "Which keyword is used to prevent method overriding?", "options": ["static", "constant", "final", "protected"], "correct_answer": "final"},
    {"category": "Java", "type": "mcq", "text": "What is the size of int variable?", "options": ["8 bit", "16 bit", "32 bit", "64 bit"], "correct_answer": "32 bit"},

    # 5 DSA Questions
    {"category": "DSA", "type": "mcq", "text": "What is the time complexity of binary search?", "options": ["O(n)", "O(log n)", "O(n^2)", "O(1)"], "correct_answer": "O(log n)"},
    {"category": "DSA", "type": "mcq", "text": "Which data structure is used for recursion?", "options": ["Queue", "Stack", "Linked List", "Tree"], "correct_answer": "Stack"},
    {"category": "DSA", "type": "mcq", "text": "What is the worst case time complexity of Quick Sort?", "options": ["O(n log n)", "O(n^2)", "O(n)", "O(log n)"], "correct_answer": "O(n^2)"},
    {"category": "DSA", "type": "mcq", "text": "Which of the following is a linear data structure?", "options": ["Tree", "Graph", "Array", "AVL Tree"], "correct_answer": "Array"},
    {"category": "DSA", "type": "mcq", "text": "In a stack, if a user tries to remove an element from an empty stack it is called?", "options": ["Underflow", "Empty collection", "Overflow", "Garbage collection"], "correct_answer": "Underflow"},

    # 4 Frontend Questions
    {"category": "Frontend", "type": "mcq", "text": "Which hook is used for side effects in React?", "options": ["useState", "useEffect", "useContext", "useReducer"], "correct_answer": "useEffect"},
    {"category": "Frontend", "type": "mcq", "text": "What does CSS stand for?", "options": ["Creative Style Sheets", "Cascading Style Sheets", "Computer Style Sheets", "Colorful Style Sheets"], "correct_answer": "Cascading Style Sheets"},
    {"category": "Frontend", "type": "mcq", "text": "Which HTML tag is used to define an internal style sheet?", "options": ["<script>", "<style>", "<css>", "<link>"], "correct_answer": "<style>"},
    {"category": "Frontend", "type": "mcq", "text": "What is the default display value of a <div> element?", "options": ["inline", "block", "inline-block", "flex"], "correct_answer": "block"},

    # 1 Subjective Question
    {"category": "Subjective", "type": "subjective", "text": "Explain the concept of Virtual DOM in React.", "options": [], "correct_answer": "The Virtual DOM is a lightweight copy of the actual DOM. React uses it to improve performance by updating only the changed parts of the real DOM."}
]

MOCK_INTERVIEW_QUESTIONS = [
    "Can you explain the difference between a process and a thread?",
    "What are the ACID properties in a database?",
    "Explain the concept of polymorphism in Object-Oriented Programming.",
    "How does a hash map work internally?",
    "What is the difference between TCP and UDP?",
    "Explain the concept of dependency injection.",
    "What is a REST API and what are its key constraints?",
    "How do you handle state management in a complex application?",
    "What is the difference between authentication and authorization?",
    "Can you describe a challenging technical problem you solved recently?"
]

def clean_json_response(content: str):
    """
    Helper to clean and extract JSON from LLM response.
    """
    content = content.strip()
    
    # Remove markdown code blocks
    if "```json" in content:
        content = content.split("```json")[1].split("```")[0].strip()
    elif "```" in content:
        content = content.split("```")[1].split("```")[0].strip()
        
    # Find the first '[' and last ']' to extract the array
    start_idx = content.find('[')
    end_idx = content.rfind(']')
    
    if start_idx != -1 and end_idx != -1:
        content = content[start_idx:end_idx+1]
        
    return content

def generate_daily_questions():
    """
    Generates 5 MCQs and 1 Subjective question using the LLM.
    """
    if not settings.OPENAI_API_KEY or settings.OPENAI_API_KEY.startswith("INSERT_YOUR"):
        # Fallback if key is not set yet
        return MOCK_QUESTIONS

    try:
        from openai import OpenAI
        client = OpenAI(
            api_key=settings.OPENAI_API_KEY,
            base_url=settings.OPENAI_API_BASE
        )
        
        prompt = """
        Generate a daily technical assessment for a Full Stack Developer.
        
        Requirements:
        1. 5 Multiple Choice Questions (MCQs) covering Java.
        2. 5 Multiple Choice Questions (MCQs) covering DSA.
        3. 5 Multiple Choice Questions (MCQs) covering OOPs.
        4. 1 Subjective Question.
        5. OUTPUT MUST BE RAW JSON ONLY. NO MARKDOWN. NO EXPLANATIONS.
        
        Response Format (JSON Array):
        [
            {"category": "Java", "type": "mcq", "text": "Question?", "options": ["A", "B", "C", "D"], "correct_answer": "Correct Option Text"},
            ...
            {"category": "DSA", "type": "mcq", "text": "Question?", "options": ["A", "B", "C", "D"], "correct_answer": "Correct Option Text"},
            ...
            {"category": "OOPs", "type": "mcq", "text": "Question?", "options": ["A", "B", "C", "D"], "correct_answer": "Correct Option Text"},
            ...
            {"category": "Subjective", "type": "subjective", "text": "Question?", "options": [], "correct_answer": "Model Answer"}
        ]
        """
        
        response = client.chat.completions.create(
            model=settings.OPENAI_MODEL_NAME,
            messages=[
                {"role": "system", "content": "You are a technical interviewer. Return strictly valid JSON array only."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        
        content = response.choices[0].message.content
        cleaned_content = clean_json_response(content)
        
        try:
            return json.loads(cleaned_content)
        except json.JSONDecodeError as e:
            print(f"JSON Parse Error: {e}")
            print(f"Failed Content: {cleaned_content[:500]}...") # Log first 500 chars
            # Try one more fallback: sometimes models use single quotes
            try:
                import ast
                return ast.literal_eval(cleaned_content)
            except:
                return MOCK_QUESTIONS
        
    except Exception as e:
        print(f"Error generating daily questions: {e}")
        return MOCK_QUESTIONS

FALLBACK_CODING_PROBLEMS = [
    {
        "title": "Two Sum",
        "description": "Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.",
        "difficulty": "Easy",
        "test_cases": [{"input": "[2,7,11,15], 9", "output": "[0,1]"}, {"input": "[3,2,4], 6", "output": "[1,2]"}]
    },
    {
        "title": "Valid Palindrome",
        "description": "A phrase is a palindrome if, after converting all uppercase letters into lowercase letters and removing all non-alphanumeric characters, it reads the same forward and backward. Given a string s, return true if it is a palindrome, or false otherwise.",
        "difficulty": "Easy",
        "test_cases": [{"input": "\"A man, a plan, a canal: Panama\"", "output": "true"}, {"input": "\"race a car\"", "output": "false"}]
    },
    {
        "title": "Reverse Linked List",
        "description": "Given the head of a singly linked list, reverse the list, and return the reversed list.",
        "difficulty": "Easy",
        "test_cases": [{"input": "[1,2,3,4,5]", "output": "[5,4,3,2,1]"}, {"input": "[1,2]", "output": "[2,1]"}]
    },
    {
        "title": "Maximum Subarray",
        "description": "Given an integer array nums, find the subarray with the largest sum, and return its sum.",
        "difficulty": "Medium",
        "test_cases": [{"input": "[-2,1,-3,4,-1,2,1,-5,4]", "output": "6"}, {"input": "[1]", "output": "1"}]
    },
    {
        "title": "Climbing Stairs",
        "description": "You are climbing a staircase. It takes n steps to reach the top. Each time you can either climb 1 or 2 steps. In how many distinct ways can you climb to the top?",
        "difficulty": "Easy",
        "test_cases": [{"input": "2", "output": "2"}, {"input": "3", "output": "3"}]
    }
]

def generate_coding_problem():
    """
    Generates a random coding problem (Easy/Medium/Hard) using LLM.
    """
    if not settings.OPENAI_API_KEY or settings.OPENAI_API_KEY.startswith("INSERT_YOUR"):
        return {
            "id": 1,
            "title": "Two Sum (Mock)",
            "description": "Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.",
            "difficulty": "Easy",
            "test_cases": [{"input": "[2,7,11,15], 9", "output": "[0,1]"}]
        }

    try:
        from openai import OpenAI
        client = OpenAI(
            api_key=settings.OPENAI_API_KEY,
            base_url=settings.OPENAI_API_BASE
        )
        
        prompt = """
        Generate a unique coding interview problem.
        
        Requirements:
        1. Title: Short and descriptive.
        2. Description: Clear problem statement.
        3. Difficulty: Randomly choose between Easy, Medium, Hard.
        4. Test Cases: Provide 2-3 example test cases.
        5. OUTPUT MUST BE RAW JSON ONLY. NO MARKDOWN.
        
        Response Format (JSON):
        {
            "title": "Problem Title",
            "description": "Full problem description...",
            "difficulty": "Medium",
            "test_cases": [
                {"input": "...", "output": "..."},
                {"input": "...", "output": "..."}
            ]
        }
        """
        
        response = client.chat.completions.create(
            model=settings.OPENAI_MODEL_NAME,
            messages=[
                {"role": "system", "content": "You are a senior technical interviewer. Return strictly valid JSON only."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.8
        )
        
        content = response.choices[0].message.content
        cleaned_content = clean_json_response(content)
        
        problem = json.loads(cleaned_content)
        problem["id"] = random.randint(100, 9999) # Generate a random ID for now
        return problem
        
    except Exception as e:
        print(f"Error generating coding problem: {e}")
        return {
            "id": 1,
            "title": "Error Generating Problem",
            "description": "Could not generate a new problem. Please try again.",
            "difficulty": "Unknown",
            "test_cases": []
        }

def generate_coding_problem():
    """
    Generates a random coding problem (Easy/Medium/Hard) using LLM.
    """
    if not settings.OPENAI_API_KEY or settings.OPENAI_API_KEY.startswith("INSERT_YOUR"):
        return {
            "id": 1,
            "title": "Two Sum (Mock)",
            "description": "Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.",
            "difficulty": "Easy",
            "test_cases": [{"input": "[2,7,11,15], 9", "output": "[0,1]"}]
        }

    for attempt in range(2): # Retry up to 2 times
        try:
            from openai import OpenAI
            client = OpenAI(
                api_key=settings.OPENAI_API_KEY,
                base_url=settings.OPENAI_API_BASE
            )
            
            prompt = """
            Generate a single unique coding interview problem.
            
            Return ONLY a raw JSON object with this exact structure:
            {
                "title": "Short Title",
                "description": "Problem statement...",
                "difficulty": "Easy/Medium/Hard",
                "test_cases": [
                    {"input": "arg1, arg2", "output": "result"},
                    {"input": "arg1, arg2", "output": "result"}
                ]
            }
            
            IMPORTANT:
            - NO Markdown formatting (no ```json).
            - NO introductory text.
            - Valid JSON only.
            """
            
            response = client.chat.completions.create(
                model=settings.OPENAI_MODEL_NAME,
                messages=[
                    {"role": "system", "content": "You are a JSON generator. Output strictly valid JSON only."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.6,
                timeout=8.0 # Strict timeout to prevent frontend hanging
            )
            
            content = response.choices[0].message.content
            cleaned_content = clean_json_response(content)
            
            try:
                problem = json.loads(cleaned_content)
            except json.JSONDecodeError:
                # Fallback for single quotes or slight malformation
                import ast
                problem = ast.literal_eval(cleaned_content)
                
            # Handle case where model returns a list instead of a dict
            if isinstance(problem, list):
                if len(problem) > 0:
                    problem = problem[0]
                else:
                    continue # Retry on empty list
                    
            if not isinstance(problem, dict):
                 continue # Retry if not a dict
    
            # Validate required keys
            required_keys = ["title", "description", "test_cases"]
            missing_keys = [key for key in required_keys if key not in problem]
            if missing_keys:
                print(f"Attempt {attempt+1} failed: Missing keys {missing_keys}")
                continue # Retry on missing keys
    
            problem["id"] = random.randint(100, 9999) # Generate a random ID for now
            return problem
            
        except Exception as e:
            print(f"Attempt {attempt+1} error: {e}")
            continue

    # If all retries fail, return a random fallback problem
    print("All retries failed. Using fallback problem.")
    fallback = random.choice(FALLBACK_CODING_PROBLEMS)
    fallback["id"] = random.randint(10000, 99999)
    return fallback

def evaluate_code(code: str, language: str, problem_title: str):
    """
    Simulates code execution and validation using LLM.
    """
    # Check if key is missing or is the default placeholder
    if not settings.OPENAI_API_KEY or settings.OPENAI_API_KEY.startswith("sk-proj-your") or settings.OPENAI_API_KEY == "CHANGE_THIS_TO_A_SECURE_RANDOM_STRING":
        # Fallback mock logic for demo without API key
        
        # 1. Basic Length Check
        if len(code.strip()) < 10:
             return {"status": "error", "output": f"Error: Code is too short to be a valid solution."}

        # 2. Language-Specific Syntax Checks
        if language.lower() == "python":
            import ast
            try:
                ast.parse(code)
            except SyntaxError as e:
                return {"status": "error", "output": f"SyntaxError: {e}"}
            
            # Check for required logic keywords (naive check)
            if "return" not in code:
                 return {"status": "error", "output": "LogicError: Solution must return a value."}

        elif language.lower() in ["java", "cpp"]:
            if "return" not in code or ";" not in code:
                return {"status": "error", "output": f"SyntaxError: Missing 'return' statement or semicolons in {language} code."}
            if "class" not in code and language == "java":
                 return {"status": "error", "output": "SyntaxError: Java solution must be within a class."}

        # 3. Random "Runtime" Error for realism if code looks okay but is just random words
        # (This is still a mock, so we can't actually run it, but this helps catch gibberish)
        common_keywords = ["def", "class", "int", "void", "vector", "import", "include"]
        if not any(keyword in code for keyword in common_keywords):
             return {"status": "error", "output": "CompilerError: Code does not appear to contain valid programming constructs."}

        return {"status": "success", "output": "Demo Mode (No API Key):\nTest Case 1: Passed\nTest Case 2: Passed\n(Note: Logic not fully verified without OpenAI Key)"}

    try:
        from openai import OpenAI
        client = OpenAI(
            api_key=settings.OPENAI_API_KEY,
            base_url=settings.OPENAI_API_BASE
        )
        
        prompt = f"""
        You are a strict code judge and compiler.
        
        Problem: {problem_title}
        Language: {language}
        
        Code:
        {code}
        
        Task:
        1. Analyze the code for Correctness, Time Complexity, and Space Complexity.
        2. Check for Syntax Errors.
        3. Simulate running against 3-4 edge cases.
        4. Provide a detailed, structured output.
        
        Response Format (JSON):
        {{
            "status": "success" or "error",
            "output": "Detailed console output...",
            "analysis": {{
                "correctness": "Passed/Failed",
                "time_complexity": "O(...)",
                "space_complexity": "O(...)",
                "feedback": "Brief feedback on code quality..."
            }}
        }}
        """
        
        response = client.chat.completions.create(
            model=settings.OPENAI_MODEL_NAME,
            messages=[
                {"role": "system", "content": "You are a code judge. Return strictly valid JSON only."},
                {"role": "user", "content": prompt}
            ]
        )
        
        content = response.choices[0].message.content
        cleaned_content = clean_json_response(content)
        
        return json.loads(cleaned_content)
            
    except Exception as e:
        print(f"Error evaluating code: {e}")
        return {"status": "error", "output": f"Evaluation Failed: {str(e)}"}

def generate_interview_followup(history: list, job_description: str, resume_text: str = ""):
    """
    Generates a follow-up interview question based on chat history and context.
    Uses a staged approach: Intro -> Role Fit -> Experience -> Technical -> Conclusion.
    """
    # Fallback function to get a random question
    def get_fallback_question():
        return random.choice(MOCK_INTERVIEW_QUESTIONS) + " (Demo Mode)"

    if not settings.OPENAI_API_KEY or settings.OPENAI_API_KEY.startswith("sk-proj-your") or settings.OPENAI_API_KEY == "CHANGE_THIS_TO_A_SECURE_RANDOM_STRING":
        return get_fallback_question()

    try:
        from openai import OpenAI
        client = OpenAI(
            api_key=settings.OPENAI_API_KEY,
            base_url=settings.OPENAI_API_BASE
        )
        
        # Determine Stage based on turn count (each turn has user+ai, so 2 messages)
        turn_count = len(history) // 2
        stage = "General Introduction"
        if turn_count < 2:
            stage = "Introduction & Ice-breaking"
        elif turn_count < 5:
            stage = "Job Role Fit & Motivation (Focus on JD)"
        elif turn_count < 8:
            stage = "Resume & Experience Deep Dive"
        elif turn_count < 12:
            stage = "Technical & Problem Solving"
        else:
            stage = "Closing & Wrap-up"

        system_prompt = f"""
        You are an expert AI Technical Interviewer. 
        Current Stage: {stage}
        
        Context:
        - Job Description: {job_description}
        - Candidate Resume: {resume_text[:2000]}... (truncated)
        
        Guidelines:
        1. Ask ONE clear, relevant question based on the current stage.
        2. Be professional but conversational.
        3. If the candidate's answer is vague, ask a follow-up.
        4. Do NOT repeat questions.
        5. Keep responses concise (under 50 words) to maintain flow.
        """
        
        messages = [{"role": "system", "content": system_prompt}]
        
        # Add conversation history
        for msg in history:
            messages.append({"role": msg["role"], "content": msg["content"]})
            
        response = client.chat.completions.create(
            model=settings.OPENAI_MODEL_NAME,
            messages=messages,
            temperature=0.7
        )
        
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error generating interview response: {e}")
        return "I apologize, but I am having trouble connecting to my brain right now. Please check the system configuration."

def generate_interview_feedback(history: list, job_description: str):
    """
    Analyzes the interview history and generates a detailed feedback report.
    """
    if not settings.OPENAI_API_KEY or settings.OPENAI_API_KEY.startswith("sk-proj-your") or settings.OPENAI_API_KEY == "CHANGE_THIS_TO_A_SECURE_RANDOM_STRING":
        return {
            "score": 85,
            "strengths": ["Good communication", "Basic knowledge of concepts"],
            "weaknesses": ["Could go deeper into technical details", "Answers were a bit short"],
            "summary": "A good initial interview. The candidate showed promise but needs to demonstrate more depth in specific technical areas related to the role."
        }

    try:
        from openai import OpenAI
        client = OpenAI(
            api_key=settings.OPENAI_API_KEY,
            base_url=settings.OPENAI_API_BASE # Will be None by default (OpenAI), or custom URL
        )
        
        prompt = f"""
        Analyze this technical interview transcript and provide a detailed assessment.
        
        Job Description: {job_description}
        
        Transcript:
        {json.dumps(history[-20:])} 
        
        Task:
        1. Rate the candidate from 0-100 based on relevance, technical depth, and communication.
        2. Identify top 3 strengths.
        3. Identify top 3 areas for improvement (weaknesses).
        4. Write a brief professional summary (2-3 sentences).
        
        Response Format (JSON):
        {{
            "score": 85,
            "strengths": ["...", "...", "..."],
            "weaknesses": ["...", "...", "..."],
            "summary": "..."
        }}
        """
        
        response = client.chat.completions.create(
            model=settings.OPENAI_MODEL_NAME,
            messages=[
                {"role": "system", "content": "You are a senior hiring manager. Return JSON only."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5
        )
        
        content = response.choices[0].message.content
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            return {
                "score": 70,
                "strengths": ["Communication"],
                "weaknesses": ["Technical Depth"],
                "summary": content[:200]
            }
            
    except Exception as e:
        print(f"Error generating feedback: {e}")
        # Return error state so frontend knows it failed
        return {
            "score": 0,
            "strengths": ["Analysis Failed"],
            "weaknesses": ["API Error or Quota Exceeded"],
            "summary": f"Could not generate feedback report. Error: {str(e)}"
        }
