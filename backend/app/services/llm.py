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

    # 5 OOPs Questions (Replaced Frontend)
    {"category": "OOPs", "type": "mcq", "text": "Which concept allows a class to derive properties from another class?", "options": ["Polymorphism", "Inheritance", "Encapsulation", "Abstraction"], "correct_answer": "Inheritance"},
    {"category": "OOPs", "type": "mcq", "text": "Which of these is an access modifier?", "options": ["protected", "void", "static", "final"], "correct_answer": "protected"},
    {"category": "OOPs", "type": "mcq", "text": "What is the process of hiding internal details and showing only functionality?", "options": ["Encapsulation", "Abstraction", "Polymorphism", "Inheritance"], "correct_answer": "Abstraction"},
    {"category": "OOPs", "type": "mcq", "text": "Which feature of OOP illustrated the code reusability?", "options": ["Polymorphism", "Abstraction", "Inheritance", "Encapsulation"], "correct_answer": "Inheritance"},
    {"category": "OOPs", "type": "mcq", "text": "Method overloading is an example of?", "options": ["Runtime Polymorphism", "Compile time Polymorphism", "Encapsulation", "Inheritance"], "correct_answer": "Compile time Polymorphism"},

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
        1. EXACTLY 5 Multiple Choice Questions (MCQs) covering "Java".
        2. EXACTLY 5 Multiple Choice Questions (MCQs) covering "DSA".
        3. EXACTLY 5 Multiple Choice Questions (MCQs) covering "OOPs".
        4. EXACTLY 1 Subjective Question covering "Subjective".
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
        
        questions = []
        try:
            questions = json.loads(cleaned_content)
        except json.JSONDecodeError as e:
            print(f"JSON Parse Error: {e}")
            # Try one more fallback: sometimes models use single quotes
            try:
                import ast
                questions = ast.literal_eval(cleaned_content)
            except:
                return MOCK_QUESTIONS

        # Post-processing to ensure categories are set
        if isinstance(questions, list):
            for i, q in enumerate(questions):
                if "category" not in q or q["category"] == "General":
                    # Infer category based on index if missing
                    if i < 5: q["category"] = "Java"
                    elif i < 10: q["category"] = "DSA"
                    elif i < 15: q["category"] = "OOPs"
                    else: q["category"] = "Subjective"
        
        return questions
        
    except Exception as e:
        print(f"Error generating daily questions: {e}")
        return MOCK_QUESTIONS

def generate_coding_problem():
    """
    Generates a random coding problem (Easy/Medium/Hard) using LLM.
    Returns an error object if generation fails (No Fallbacks).
    """
    if not settings.OPENAI_API_KEY or settings.OPENAI_API_KEY.startswith("INSERT_YOUR"):
        return {
            "id": 1,
            "title": "API Key Missing",
            "description": "Please configure a valid OpenAI/SambaNova API key in .env to generate coding problems.",
            "difficulty": "System",
            "test_cases": []
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
                timeout=8.0 # Strict timeout
            )
            
            content = response.choices[0].message.content
            cleaned_content = clean_json_response(content)
            
            try:
                problem = json.loads(cleaned_content)
            except json.JSONDecodeError:
                import ast
                problem = ast.literal_eval(cleaned_content)
                
            if isinstance(problem, list):
                if len(problem) > 0: problem = problem[0]
                else: continue
                    
            if not isinstance(problem, dict): continue
    
            required_keys = ["title", "description", "test_cases"]
            if any(key not in problem for key in required_keys):
                continue
    
            problem["id"] = random.randint(100, 9999)
            return problem
            
        except Exception as e:
            print(f"Attempt {attempt+1} error: {e}")
            continue

    # If all retries fail, return error object (No Fallback Questions)
    return {
        "id": 1,
        "title": "Generation Failed",
        "description": "Could not generate a new problem. This is likely due to an API Key expiry or connection issue. Please check your API configuration.",
        "difficulty": "Error",
        "test_cases": []
    }

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
