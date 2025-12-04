import openai
from app.core.config import settings
import json
import random

# Extended Mock response to meet new requirements
# Mock data removed to enforce strict API usage

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

# ... (imports remain the same)

def is_valid_api_key():
    """
    Checks if a valid API key is configured.
    Returns True if key exists and is not a placeholder.
    """
    key = settings.OPENAI_API_KEY
    if not key:
        return False
    
    # Check for common placeholders
    placeholders = [
        "INSERT_YOUR", 
        "sk-proj-your", 
        "CHANGE_THIS", 
        "YOUR_API_KEY"
    ]
    
    if any(p in key for p in placeholders):
        return False
        
    return True

# ... (imports remain the same)

def is_valid_api_key():
    """
    Checks if a valid API key is configured.
    Returns True if key exists and is not a placeholder.
    """
    key = settings.OPENAI_API_KEY
    if not key:
        return False
    
    # Check for common placeholders
    placeholders = [
        "INSERT_YOUR", 
        "sk-proj-your", 
        "CHANGE_THIS", 
        "YOUR_API_KEY"
    ]
    
    if any(p in key for p in placeholders):
        return False
        
    return True

def generate_daily_questions():
    """
    Generates 5 MCQs and 1 Subjective question using the LLM.
    Raises Exception if generation fails (No Mock Data).
    """
    if not is_valid_api_key():
        raise Exception("OpenAI API Key is missing or invalid. Please configure it in .env to generate questions.")

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
                raise Exception("Failed to parse LLM response for questions.")

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
        error_msg = str(e)
        if "429" in error_msg:
            print(f"Rate Limit Exceeded: {error_msg}")
            raise Exception("API Rate Limit Exceeded. Please check your API quota or try again later.")
        print(f"Error generating daily questions: {e}")
        raise e # Re-raise to prevent fallback

def generate_coding_problem():
    """
    Generates a random coding problem (Easy/Medium/Hard) using LLM.
    Returns an error object if generation fails (No Fallbacks).
    """
    if not is_valid_api_key():
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
            error_msg = str(e)
            if "429" in error_msg:
                return {
                    "id": 1,
                    "title": "Rate Limit Exceeded",
                    "description": "Your API key has hit its rate limit. Please check your quota or try again later.",
                    "difficulty": "Error",
                    "test_cases": []
                }
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
    if not is_valid_api_key():
        return {"status": "error", "output": "API Key missing. Cannot evaluate code."}

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
        error_msg = str(e)
        if "429" in error_msg:
             return {"status": "error", "output": "API Rate Limit Exceeded. Please check your quota."}
        print(f"Error evaluating code: {e}")
        return {"status": "error", "output": f"Evaluation Failed: {str(e)}"}

def generate_interview_followup(history: list, job_description: str, resume_text: str = ""):
    """
    Generates a follow-up interview question based on chat history and context.
    Uses a staged approach: Intro -> Role Fit -> Experience -> Technical -> Conclusion.
    """
    if not is_valid_api_key():
        return "Error: AI Interviewer is offline (API Key missing)."

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
        error_msg = str(e)
        if "429" in error_msg:
            return "Error: API Rate Limit Exceeded. Please check your system configuration."
        print(f"Error generating interview response: {e}")
        return f"Error: {str(e)}"

def generate_interview_feedback(history: list, job_description: str):
    """
    Analyzes the interview history and generates a detailed feedback report.
    """
    if not is_valid_api_key():
        return {
            "score": 0,
            "strengths": ["API Key Missing"],
            "weaknesses": ["Cannot generate feedback"],
            "summary": "Please configure a valid API key to receive feedback."
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
        error_msg = str(e)
        if "429" in error_msg:
            return {
                "score": 0,
                "strengths": ["Rate Limit Exceeded"],
                "weaknesses": ["Please check API quota"],
                "summary": "Could not generate feedback due to API rate limits."
            }
        print(f"Error generating feedback: {e}")
        # Return error state so frontend knows it failed
        return {
            "score": 0,
            "strengths": ["Analysis Failed"],
            "weaknesses": ["API Error or Quota Exceeded"],
            "summary": f"Could not generate feedback report. Error: {str(e)}"
        }
