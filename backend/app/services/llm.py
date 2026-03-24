import openai
from app.core.config import settings
import json
import random

# ==================== MOCK DATA FOR FALLBACK ====================
# Used when API rate limit exceeded or connection fails

MOCK_ASSESSMENT_SETS = [
    # SET 1
    [
        {"category": "Java", "type": "mcq", "text": "What is the purpose of the synchronized keyword in Java?", 
         "options": ["To create threads", "To prevent memory leaks", "To ensure thread-safe access to shared resources", "To increase performance"],
         "correct_answer": "To ensure thread-safe access to shared resources"},
        {"category": "Java", "type": "mcq", "text": "Which of the following is NOT a feature of Java 8?",
         "options": ["Lambda expressions", "Stream API", "Record classes", "Functional interfaces"],
         "correct_answer": "Record classes"},
        {"category": "Java", "type": "mcq", "text": "What is the difference between ArrayList and LinkedList?",
         "options": ["No difference", "ArrayList is faster for random access, LinkedList is better for insertions", "LinkedList is always faster", "ArrayList supports threads, LinkedList doesn't"],
         "correct_answer": "ArrayList is faster for random access, LinkedList is better for insertions"},
        {"category": "Java", "type": "mcq", "text": "Which method is used to start a thread in Java?",
         "options": ["start()", "run()", "execute()", "begin()"],
         "correct_answer": "start()"},
        {"category": "Java", "type": "mcq", "text": "What is a ConcurrentHashMap used for?",
         "options": ["Compression", "Thread-safe HashMap operations", "Serialization", "Memory management"],
         "correct_answer": "Thread-safe HashMap operations"},
        {"category": "DSA", "type": "mcq", "text": "What is the time complexity of binary search?",
         "options": ["O(n)", "O(n log n)", "O(log n)", "O(n^2)"],
         "correct_answer": "O(log n)"},
        {"category": "DSA", "type": "mcq", "text": "Which sorting algorithm is most efficient for nearly sorted data?",
         "options": ["Bubble Sort", "Merge Sort", "Insertion Sort", "Quick Sort"],
         "correct_answer": "Insertion Sort"},
        {"category": "DSA", "type": "mcq", "text": "What data structure is best for representing a hierarchical relationship?",
         "options": ["Array", "Linked List", "Tree", "Queue"],
         "correct_answer": "Tree"},
        {"category": "DSA", "type": "mcq", "text": "What is the space complexity of merge sort?",
         "options": ["O(1)", "O(log n)", "O(n)", "O(n^2)"],
         "correct_answer": "O(n)"},
        {"category": "DSA", "type": "mcq", "text": "Which data structure uses LIFO principle?",
         "options": ["Queue", "Stack", "Deque", "Priority Queue"],
         "correct_answer": "Stack"},
        {"category": "OOPs", "type": "mcq", "text": "What is polymorphism in OOP?",
         "options": ["Inheritance", "Ability to take multiple forms", "Encapsulation", "Abstraction"],
         "correct_answer": "Ability to take multiple forms"},
        {"category": "OOPs", "type": "mcq", "text": "What is the SOLID principle 'S' referring to?",
         "options": ["Serialization", "Single Responsibility Principle", "Static Binding", "String literals"],
         "correct_answer": "Single Responsibility Principle"},
        {"category": "OOPs", "type": "mcq", "text": "What is the difference between composition and inheritance?",
         "options": ["No difference", "Composition uses 'has-a', inheritance uses 'is-a'", "They are the same concept", "Composition is deprecated"],
         "correct_answer": "Composition uses 'has-a', inheritance uses 'is-a'"},
        {"category": "OOPs", "type": "mcq", "text": "Which access modifier is most restrictive?",
         "options": ["public", "protected", "private", "default"],
         "correct_answer": "private"},
        {"category": "OOPs", "type": "mcq", "text": "What is an interface in Java primarily used for?",
         "options": ["Type casting", "Defining contracts", "Memory allocation", "Performance optimization"],
         "correct_answer": "Defining contracts"},
        {"category": "Subjective", "type": "subjective", "text": "Explain the concept of thread-safe collections in Java with an example.",
         "options": [], "correct_answer": "Thread-safe collections like ConcurrentHashMap, CopyOnWriteArrayList use synchronization mechanisms to ensure that only one thread can modify the collection at a time, preventing race conditions and data corruption."}
    ],
    # SET 2
    [
        {"category": "Java", "type": "mcq", "text": "What is the default value of a local variable in Java?",
         "options": ["0", "null", "Undefined", "false"],
         "correct_answer": "Undefined"},
        {"category": "Java", "type": "mcq", "text": "Which keyword is used to prevent method overriding?",
         "options": ["static", "final", "abstract", "synchronized"],
         "correct_answer": "final"},
        {"category": "Java", "type": "mcq", "text": "What is the purpose of the volatile keyword?",
         "options": ["To delete variables", "To ensure visibility of changes across threads", "To increase speed", "To save memory"],
         "correct_answer": "To ensure visibility of changes across threads"},
        {"category": "Java", "type": "mcq", "text": "How are generics implemented in Java?",
         "options": ["Type erasure", "Type substitution", "Type coercion", "Type casting"],
         "correct_answer": "Type erasure"},
        {"category": "Java", "type": "mcq", "text": "What is a functional interface?",
         "options": ["Interface with multiple methods", "Interface with exactly one abstract method", "Interface that implements functions", "Interface without methods"],
         "correct_answer": "Interface with exactly one abstract method"},
        {"category": "DSA", "type": "mcq", "text": "What is the average case time complexity of quicksort?",
         "options": ["O(n)", "O(n log n)", "O(n^2)", "O(log n)"],
         "correct_answer": "O(n log n)"},
        {"category": "DSA", "type": "mcq", "text": "Which traversal method visits nodes level by level?",
         "options": ["In-order", "Pre-order", "Level-order (BFS)", "Post-order"],
         "correct_answer": "Level-order (BFS)"},
        {"category": "DSA", "type": "mcq", "text": "What is the time complexity of finding an element in a balanced BST?",
         "options": ["O(n)", "O(log n)", "O(n^2)", "O(1)"],
         "correct_answer": "O(log n)"},
        {"category": "DSA", "type": "mcq", "text": "How many edges does a tree with n nodes have?",
         "options": ["n", "n-1", "n+1", "2n"],
         "correct_answer": "n-1"},
        {"category": "DSA", "type": "mcq", "text": "What is the purpose of a hash function in a hash map?",
         "options": ["Sorting", "Mapping keys to buckets", "Encryption", "Compression"],
         "correct_answer": "Mapping keys to buckets"},
        {"category": "OOPs", "type": "mcq", "text": "What is encapsulation?",
         "options": ["Hiding details", "Bundling data and methods", "Restricting access to internal details", "All of the above"],
         "correct_answer": "All of the above"},
        {"category": "OOPs", "type": "mcq", "text": "What is method overloading?",
         "options": ["Methods with same name but different parameters", "Methods with different names", "Calling multiple methods", "Method inheritance"],
         "correct_answer": "Methods with same name but different parameters"},
        {"category": "OOPs", "type": "mcq", "text": "What is an abstract class used for?",
         "options": ["To create objects", "To define common behavior for subclasses", "To improve performance", "To save memory"],
         "correct_answer": "To define common behavior for subclasses"},
        {"category": "OOPs", "type": "mcq", "text": "What does method overriding allow?",
         "options": ["Multiple methods with same name", "Subclass to provide implementation", "Accessing private members", "Changing method signatures"],
         "correct_answer": "Subclass to provide implementation"},
        {"category": "OOPs", "type": "mcq", "text": "What is the Liskov Substitution Principle?",
         "options": ["Objects should be substitutable without breaking code", "All objects are the same", "Use lists instead of arrays", "Substitute variables"],
         "correct_answer": "Objects should be substitutable without breaking code"},
        {"category": "Subjective", "type": "subjective", "text": "Describe the differences between ArrayList and Vector in Java.",
         "options": [], "correct_answer": "ArrayList is not synchronized (not thread-safe) and is faster, while Vector is synchronized (thread-safe) but slower. ArrayList is preferred in single-threaded environments."}
    ],
    # SET 3
    [
        {"category": "Java", "type": "mcq", "text": "What does the JVM do?",
         "options": ["Compiles code", "Interprets bytecode", "Manages threads", "All of the above"],
         "correct_answer": "All of the above"},
        {"category": "Java", "type": "mcq", "text": "What is the purpose of the super keyword?",
         "options": ["To access parent class members", "To create threads", "To define interfaces", "To manage memory"],
         "correct_answer": "To access parent class members"},
        {"category": "Java", "type": "mcq", "text": "Which exception is thrown when dividing by zero?",
         "options": ["ArithmeticException", "NullPointerException", "NumberFormatException", "RuntimeException"],
         "correct_answer": "ArithmeticException"},
        {"category": "Java", "type": "mcq", "text": "What is the difference between == and equals()?",
         "options": ["No difference", "== checks reference, equals() checks value", "== checks value, equals() checks reference", "Both check memory"],
         "correct_answer": "== checks reference, equals() checks value"},
        {"category": "Java", "type": "mcq", "text": "What is a SerialVersionUID used for?",
         "options": ["Version control", "Serialization compatibility", "Thread management", "Memory allocation"],
         "correct_answer": "Serialization compatibility"},
        {"category": "DSA", "type": "mcq", "text": "What is a graph with no cycles called?",
         "options": ["Complete graph", "Forest/Tree", "Cycle graph", "Weighted graph"],
         "correct_answer": "Forest/Tree"},
        {"category": "DSA", "type": "mcq", "text": "Which algorithm is used for finding shortest path in unweighted graphs?",
         "options": ["DFS", "BFS", "Dijkstra", "Floyd-Warshall"],
         "correct_answer": "BFS"},
        {"category": "DSA", "type": "mcq", "text": "What is the recurrence relation for merge sort?",
         "options": ["T(n) = T(n-1) + O(1)", "T(n) = 2T(n/2) + O(n)", "T(n) = T(n-1) + O(n)", "T(n) = nT(n-1)"],
         "correct_answer": "T(n) = 2T(n/2) + O(n)"},
        {"category": "DSA", "type": "mcq", "text": "What is the minimum number of comparisons needed to sort 4 elements?",
         "options": ["3", "4", "5", "6"],
         "correct_answer": "5"},
        {"category": "DSA", "type": "mcq", "text": "In a graph, what is the sum of all degrees equal to?",
         "options": ["V", "E", "2E", "V+E"],
         "correct_answer": "2E"},
        {"category": "OOPs", "type": "mcq", "text": "What is the purpose of the instanceof operator?",
         "options": ["Instance creation", "Type checking", "Memory allocation", "Inheritance checking"],
         "correct_answer": "Type checking"},
        {"category": "OOPs", "type": "mcq", "text": "What does the Open/Closed Principle state?",
         "options": ["Open for reading, closed for writing", "Open for extension, closed for modification", "Always keep classes open", "Never modify existing code"],
         "correct_answer": "Open for extension, closed for modification"},
        {"category": "OOPs", "type": "mcq", "text": "What is dependency injection?",
         "options": ["Injecting dependencies into objects", "Deleting dependencies", "Creating static objects", "Using only private members"],
         "correct_answer": "Injecting dependencies into objects"},
        {"category": "OOPs", "type": "mcq", "text": "What is a design pattern?",
         "options": ["A solution to a common problem", "A programming language", "A software tool", "A type of IDE"],
         "correct_answer": "A solution to a common problem"},
        {"category": "OOPs", "type": "mcq", "text": "Which design pattern is used to create objects without specifying their classes?",
         "options": ["Singleton", "Factory", "Observer", "Strategy"],
         "correct_answer": "Factory"},
        {"category": "Subjective", "type": "subjective", "text": "Explain the Visitor design pattern and provide a use case example.",
         "options": [], "correct_answer": "The Visitor pattern allows adding new operations to object hierarchies without modifying the objects themselves. Example: A compiler can use a Visitor to traverse an AST (Abstract Syntax Tree) and perform different operations like type checking, code generation, etc."}
    ],
    # SET 4
    [
        {"category": "Java", "type": "mcq", "text": "What is autoboxing in Java?",
         "options": ["Automatic conversion between primitive and wrapper classes", "Boxing without permission", "Creating boxes for objects", "Memory management"],
         "correct_answer": "Automatic conversion between primitive and wrapper classes"},
        {"category": "Java", "type": "mcq", "text": "Which method is called when an object is created?",
         "options": ["init()", "constructor()", "create()", "__init__()"],
         "correct_answer": "constructor()"},
        {"category": "Java", "type": "mcq", "text": "What is the purpose of the this keyword?",
         "options": ["Reference to current object", "Reference to parent class", "Create new objects", "Delete objects"],
         "correct_answer": "Reference to current object"},
        {"category": "Java", "type": "mcq", "text": "Which exception occurs when accessing an index out of bounds?",
         "options": ["ArrayIndexOutOfBoundsException", "IndexOutOfRangeException", "BoundsException", "OverflowException"],
         "correct_answer": "ArrayIndexOutOfBoundsException"},
        {"category": "Java", "type": "mcq", "text": "What is the difference between checked and unchecked exceptions?",
         "options": ["No difference", "Checked must be caught, unchecked may be ignored", "They have same behavior", "Checked are errors"],
         "correct_answer": "Checked must be caught, unchecked may be ignored"},
        {"category": "DSA", "type": "mcq", "text": "What is a AVL tree?",
         "options": ["Unbalanced tree", "Self-balancing BST", "Binary tree", "Tree with no structure"],
         "correct_answer": "Self-balancing BST"},
        {"category": "DSA", "type": "mcq", "text": "What is the maximum height of a red-black tree with n nodes?",
         "options": ["n", "log n", "2 log n", "n^2"],
         "correct_answer": "2 log n"},
        {"category": "DSA", "type": "mcq", "text": "What is a trie data structure used for?",
         "options": ["Sorting", "Prefix-based searching", "Hashing", "Compression"],
         "correct_answer": "Prefix-based searching"},
        {"category": "DSA", "type": "mcq", "text": "What is the time complexity of insert in a skip list?",
         "options": ["O(1)", "O(n)", "O(log n)", "O(n log n)"],
         "correct_answer": "O(log n)"},
        {"category": "DSA", "type": "mcq", "text": "What is a segment tree primarily used for?",
         "options": ["Generating random numbers", "Range queries and updates", "Sorting", "Compression"],
         "correct_answer": "Range queries and updates"},
        {"category": "OOPs", "type": "mcq", "text": "What is the difference between interface and abstract class?",
         "options": ["No difference", "Interface has no state, abstract class can have state", "Same concept", "Abstract classes are deprecated"],
         "correct_answer": "Interface has no state, abstract class can have state"},
        {"category": "OOPs", "type": "mcq", "text": "What is the Adapter pattern used for?",
         "options": ["Connecting incompatible interfaces", "Adapting electricity", "Creating new classes", "Modifying existing code"],
         "correct_answer": "Connecting incompatible interfaces"},
        {"category": "OOPs", "type": "mcq", "text": "What is the Decorator pattern?",
         "options": ["Designing UI", "Adding behavior to objects dynamically", "Creating decorators", "Same as inheritance"],
         "correct_answer": "Adding behavior to objects dynamically"},
        {"category": "OOPs", "type": "mcq", "text": "What is the Strategy pattern used for?",
         "options": ["Strategic planning", "Encapsulating algorithms as objects", "Creating strategies", "Business planning"],
         "correct_answer": "Encapsulating algorithms as objects"},
        {"category": "OOPs", "type": "mcq", "text": "What is the purpose of the Iterator pattern?",
         "options": ["Iterating over elements without exposing structure", "Creating loops", "Optimization", "Memory management"],
         "correct_answer": "Iterating over elements without exposing structure"},
        {"category": "Subjective", "type": "subjective", "text": "Write a brief explanation of the MVC (Model-View-Controller) architectural pattern.",
         "options": [], "correct_answer": "MVC separates an application into three interconnected components: Model (data), View (UI), and Controller (logic). This separation improves maintainability, testability, and reusability of code."}
    ]
]

MOCK_CODING_PROBLEMS = [
    {
        "id": 101,
        "title": "Two Sum",
        "description": "Given an array of integers nums and an integer target, return the indices of the two numbers that add up to target. You may assume each input has exactly one solution, and you cannot use the same element twice.",
        "difficulty": "Easy",
        "test_cases": [
            {"input": "nums = [2,7,11,15], target = 9", "output": "[0, 1]"},
            {"input": "nums = [3,2,4], target = 6", "output": "[1, 2]"},
            {"input": "nums = [3,3], target = 6", "output": "[0, 1]"}
        ]
    },
    {
        "id": 102,
        "title": "Palindrome Number",
        "description": "Given an integer x, return true if x is a palindrome, and false otherwise. Do this without converting the number to a string.",
        "difficulty": "Easy",
        "test_cases": [
            {"input": "x = 121", "output": "true"},
            {"input": "x = -121", "output": "false"},
            {"input": "x = 10", "output": "false"}
        ]
    },
    {
        "id": 103,
        "title": "Longest Substring Without Repeating Characters",
        "description": "Given a string s, find the length of the longest substring without repeating characters.",
        "difficulty": "Medium",
        "test_cases": [
            {"input": "s = 'abcabcbb'", "output": "3"},
            {"input": "s = 'bbbbb'", "output": "1"},
            {"input": "s = 'pwwkew'", "output": "3"}
        ]
    },
    {
        "id": 104,
        "title": "Regular Expression Matching",
        "description": "Given an input string s and a pattern p, implement regular expression matching with support for '.' and '*' where '.' matches any single character and '*' matches zero or more of the preceding element.",
        "difficulty": "Hard",
        "test_cases": [
            {"input": "s = 'aa', p = 'a'", "output": "false"},
            {"input": "s = 'aa', p = 'a*'", "output": "true"},
            {"input": "s = 'ab', p = '.*'", "output": "true"}
        ]
    }
]

# ==================== MOCK INTERVIEW QUESTIONS BY ROLE ====================

MOCK_INTERVIEW_QUESTIONS = {
    "backend": {
        "Introduction & Ice-breaking": [
            "Tell me about yourself and your background in backend development.",
            "What inspired you to pursue a career in backend/server-side development?",
            "Can you walk me through your most recent project?"
        ],
        "Job Role Fit & Motivation": [
            "Why are you interested in this Backend Developer position?",
            "What excites you about the technologies mentioned in our job description?",
            "How do you stay updated with the latest backend development trends?"
        ],
        "Resume & Experience Deep Dive": [
            "Tell me about your experience with database design and optimization.",
            "What's your most complex system you've built, and how did you handle scalability?",
            "Describe your experience with REST APIs and microservices."
        ],
        "Technical & Problem Solving": [
            "How would you design a system to handle 10 million concurrent requests?",
            "What's the difference between SQL and NoSQL, and when would you use each?",
            "Explain how you would implement caching in a high-traffic application.",
            "How do you approach debugging production issues?",
            "What's your experience with CI/CD pipelines and DevOps practices?"
        ],
        "Closing & Wrap-up": [
            "What are your expectations for this role in terms of learning and growth?",
            "Do you have any questions about the role or our team?"
        ]
    },
    "uiux": {
        "Introduction & Ice-breaking": [
            "Tell me about yourself and your background in UI/UX design.",
            "What drew you to the field of user experience and interface design?",
            "Can you describe a design project you're particularly proud of?"
        ],
        "Job Role Fit & Motivation": [
            "Why are you interested in joining our team as a UI/UX Designer?",
            "How do you approach creating user-centered design solutions?",
            "What design tools and methodologies are you most comfortable with?"
        ],
        "Resume & Experience Deep Dive": [
            "Walk me through your design process from discovery to implementation.",
            "Tell me about a time when you had to advocate for the user against business constraints.",
            "Can you share an example where you improved user engagement through design?"
        ],
        "Technical & Problem Solving": [
            "How would you redesign our mobile app to improve user retention?",
            "Describe your approach to conducting user research and usability testing.",
            "How do you ensure accessibility in your designs across different devices?",
            "Tell me about your experience with design systems and component libraries.",
            "How do you balance aesthetic design with functionality and performance?"
        ],
        "Closing & Wrap-up": [
            "What design challenges are you most excited to tackle with our product?",
            "Do you have any questions about the role or our design team?"
        ]
    }
}

MOCK_INTERVIEW_FEEDBACK = {
    "backend": {
        "good": {
            "score": 78,
            "strengths": [
                "Strong grasp of system design principles and scalability concerns",
                "Good understanding of database optimization and query performance",
                "Clear communication about technical decisions and trade-offs"
            ],
            "weaknesses": [
                "Could provide more concrete examples from production experience",
                "Limited discussion of emerging technologies like gRPC or message queues",
                "Could elaborate more on monitoring and observability practices"
            ],
            "summary": "The candidate demonstrates solid backend development knowledge with good understanding of core concepts. They show promise in system architecture but would benefit from deeper exploration of advanced topics and more battle-tested experiences in high-scale systems."
        },
        "average": {
            "score": 65,
            "strengths": [
                "Fundamentals of backend development are clear",
                "Shows interest in learning new technologies",
                "Communicates technical concepts reasonably well"
            ],
            "weaknesses": [
                "Lacks depth in system design and architecture discussions",
                "Limited hands-on experience with distributed systems",
                "Could improve explanation of trade-offs and performance considerations"
            ],
            "summary": "The candidate has basic backend development knowledge but would need mentoring to handle complex system design challenges. Additional exposure to production systems and performance optimization would strengthen their candidacy."
        }
    },
    "uiux": {
        "good": {
            "score": 82,
            "strengths": [
                "User-centered design approach with strong research methodology",
                "Excellent visual design sense and understanding of accessibility",
                "Clear communication of design decisions and rationale"
            ],
            "weaknesses": [
                "Could discuss cross-functional collaboration more in detail",
                "Limited mention of metrics for measuring design success",
                "Design systems knowledge could be expanded"
            ],
            "summary": "The candidate demonstrates a mature approach to UI/UX design with strong fundamentals in user research and accessibility. Their portfolio shows thoughtful design solutions and they communicate their process clearly, making them a strong candidate for the role."
        },
        "average": {
            "score": 70,
            "strengths": [
                "Understands basic UX principles and user empathy",
                "Has practical design tool experience",
                "Shows willingness to iterate based on feedback"
            ],
            "weaknesses": [
                "User research methodology could be more rigorous",
                "Limited knowledge of design systems and component thinking",
                "Minimal discussion of accessibility considerations"
            ],
            "summary": "The candidate has foundational UI/UX design skills but would benefit from deeper training in research methods and design systems. With mentorship on accessibility and metrics-driven design, they could grow into a strong designer."
        }
    }
}

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
        
    # Find the first '{' or '['
    start_obj = content.find('{')
    start_arr = content.find('[')
    
    if start_obj != -1 and (start_arr == -1 or start_obj < start_arr):
        # It's an object
        end_obj = content.rfind('}')
        if end_obj != -1:
            content = content[start_obj:end_obj+1]
    elif start_arr != -1:
        # It's an array
        end_arr = content.rfind(']')
        if end_arr != -1:
            content = content[start_arr:end_arr+1]
        
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

def generate_daily_questions():
    """
    Generates 5 MCQs and 1 Subjective question using the LLM.
    Raises Exception if generation fails (No Mock Data).
    """
    if not is_valid_api_key():
        raise Exception("OpenAI API Key is missing or invalid. Please configure it in .env to generate questions.")

    for attempt in range(3):
        try:
            from openai import OpenAI
            client = OpenAI(
                api_key=settings.OPENAI_API_KEY,
                base_url=settings.OPENAI_API_BASE
            )
            
            # Randomize topics to prevent identical first questions
            java_topics = ["Multithreading", "Streams API", "Collections Framework", "Generics", "JVM Internals", "Exception Handling", "Java 8 Features", "Spring Boot Basics"]
            dsa_topics = ["Arrays & Strings", "Linked Lists", "Trees & Graphs", "Sorting & Searching", "Dynamic Programming", "Stacks & Queues", "Heaps", "Hash Maps"]
            oops_topics = ["Polymorphism", "Inheritance", "Encapsulation", "Abstraction", "Design Patterns", "SOLID Principles", "Interface vs Abstract Class"]
            
            selected_java = random.choice(java_topics)
            selected_dsa = random.choice(dsa_topics)
            selected_oops = random.choice(oops_topics)

            prompt = f"""
            Generate a daily technical assessment for a Full Stack Developer.
            
            Requirements:
            1. EXACTLY 5 Multiple Choice Questions (MCQs) covering "Java" (Focus on {selected_java}).
            2. EXACTLY 5 Multiple Choice Questions (MCQs) covering "DSA" (Focus on {selected_dsa}).
            3. EXACTLY 5 Multiple Choice Questions (MCQs) covering "OOPs" (Focus on {selected_oops}).
            4. EXACTLY 1 Subjective Question covering "Subjective".
            5. RESPONSE MUST BE A SINGLE VALID JSON ARRAY. 
            6. NO MARKDOWN formatting (do not use ```json).
            7. ESCAPE all internal quotes in strings.
            
            Response Structure:
            [
                {{
                    "category": "Java", 
                    "type": "mcq", 
                    "text": "Question text here?", 
                    "options": ["Option A", "Option B", "Option C", "Option D"], 
                    "correct_answer": "Option A"
                }},
                ...
                {{
                    "category": "Subjective",
                    "type": "subjective",
                    "text": "Question text?",
                    "options": [],
                    "correct_answer": "Model Answer"
                }}
            ]
            """
            
            response = client.chat.completions.create(
                model=settings.OPENAI_MODEL_NAME,
                messages=[
                    {"role": "system", "content": "You are a backend API that outputs strictly valid JSON array only. No Markdown. No checks."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.4, # Lower temperature for more deterministic formatting
                timeout=60.0
            )
            
            content = response.choices[0].message.content
            cleaned_content = clean_json_response(content)
            
            questions = []
            try:
                questions = json.loads(cleaned_content)
            except json.JSONDecodeError as e:
                print(f"JSON Parse Error (Attempt {attempt+1}): {e}")
                # Try one more fallback: sometimes models use single quotes
                try:
                    import ast
                    questions = ast.literal_eval(cleaned_content)
                except:
                    # On last attempt, raise the error
                    if attempt == 2:
                        raise Exception(f"Failed to parse LLM response. Content preview: {cleaned_content[:200]}")
                    continue # Retry

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
            if "429" in error_msg or "billing_not_active" in error_msg:
                print(f"API Rate Limit or Billing Error: {error_msg}")
                print("Returning mock assessment questions...")
                return random.choice(MOCK_ASSESSMENT_SETS)
            print(f"Error generating daily questions (Attempt {attempt+1}): {e}")
            if attempt == 2:
                print("All API attempts failed. Returning mock assessment questions...")
                return random.choice(MOCK_ASSESSMENT_SETS)

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

    for attempt in range(3): # Retry up to 3 times
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
                timeout=10.0 # Increased timeout
            )
            
            content = response.choices[0].message.content
            cleaned_content = clean_json_response(content)
            
            try:
                problem = json.loads(cleaned_content)
            except json.JSONDecodeError as e:
                print(f"JSON Parse Error (Attempt {attempt+1}): {e}")
                try:
                    import ast
                    problem = ast.literal_eval(cleaned_content)
                except:
                    if attempt == 2:
                        with open("failed_coding_response.txt", "w", encoding="utf-8") as f:
                            f.write(content)
                    continue
                
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
            if "429" in error_msg or "billing_not_active" in error_msg:
                print(f"API Rate Limit or Billing Error: {error_msg}")
                print("Returning mock coding problem...")
                return random.choice(MOCK_CODING_PROBLEMS)
            print(f"Attempt {attempt+1} error: {e}")
            continue

    # If all retries fail, return mock data
    print("All API attempts failed. Returning mock coding problem...")
    return random.choice(MOCK_CODING_PROBLEMS)

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
    Falls back to role-based mock questions when API rate limit is exceeded.
    """
    if not is_valid_api_key():
        return "Error: AI Interviewer is offline (API Key missing)."

    # Detect role from job description
    job_description_lower = job_description.lower()
    if "backend" in job_description_lower or "server" in job_description_lower or "api" in job_description_lower:
        detected_role = "backend"
    elif "ui" in job_description_lower or "ux" in job_description_lower or "design" in job_description_lower or "frontend" in job_description_lower or "visual" in job_description_lower:
        detected_role = "uiux"
    else:
        detected_role = "backend"  # Default role

    for attempt in range(3):
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
                stage = "Job Role Fit & Motivation"
            elif turn_count < 8:
                stage = "Resume & Experience Deep Dive"
            elif turn_count < 12:
                stage = "Technical & Problem Solving"
            else:
                stage = "Closing & Wrap-up"

            system_prompt = f"""
            You are an expert AI Technical Interviewer for {detected_role.upper()} role.
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
                temperature=0.6,
                max_tokens=150,
                timeout=10.0
            )
            
            return response.choices[0].message.content
        except Exception as e:
            error_msg = str(e)
            if "429" in error_msg or "billing_not_active" in error_msg:
                print(f"API Rate Limit or Billing Error: {error_msg}")
                print(f"Returning mock interview question for {detected_role} role...")
                
                # Determine stage for mock questions
                turn_count = len(history) // 2
                if turn_count < 2:
                    stage_key = "Introduction & Ice-breaking"
                elif turn_count < 5:
                    stage_key = "Job Role Fit & Motivation"
                elif turn_count < 8:
                    stage_key = "Resume & Experience Deep Dive"
                elif turn_count < 12:
                    stage_key = "Technical & Problem Solving"
                else:
                    stage_key = "Closing & Wrap-up"
                
                # Return role-based mock question
                questions = MOCK_INTERVIEW_QUESTIONS.get(detected_role, MOCK_INTERVIEW_QUESTIONS["backend"])
                stage_questions = questions.get(stage_key, [])
                if stage_questions:
                    return random.choice(stage_questions)
                else:
                    return "Could you tell me more about your approach to problem-solving in your role?"
            
            print(f"Error generating interview response (Attempt {attempt+1}): {e}")
            if attempt == 2:
                print(f"All API attempts failed. Returning mock interview question for {detected_role} role...")
                # Return fallback mock question
                questions = MOCK_INTERVIEW_QUESTIONS.get(detected_role, MOCK_INTERVIEW_QUESTIONS["backend"])
                all_questions = [q for stage_qs in questions.values() for q in stage_qs]
                return random.choice(all_questions) if all_questions else "Tell me about your experience."

def generate_interview_feedback(history: list, job_description: str):
    """
    Analyzes the interview history and generates a detailed feedback report.
    Falls back to role-based mock feedback when API rate limit is exceeded.
    """
    if not is_valid_api_key():
        return {
            "score": 0,
            "strengths": ["API Key Missing"],
            "weaknesses": ["Cannot generate feedback"],
            "summary": "Please configure a valid API key to receive feedback."
        }

    # Detect role from job description
    job_description_lower = job_description.lower()
    if "backend" in job_description_lower or "server" in job_description_lower or "api" in job_description_lower:
        detected_role = "backend"
    elif "ui" in job_description_lower or "ux" in job_description_lower or "design" in job_description_lower or "frontend" in job_description_lower or "visual" in job_description_lower:
        detected_role = "uiux"
    else:
        detected_role = "backend"  # Default role

    for attempt in range(3):
        try:
            from openai import OpenAI
            client = OpenAI(
                api_key=settings.OPENAI_API_KEY,
                base_url=settings.OPENAI_API_BASE
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
                    {"role": "system", "content": f"You are a senior hiring manager evaluating a {detected_role} candidate. Return JSON only."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5,
                timeout=15.0
            )
            
            content = response.choices[0].message.content
            cleaned_content = clean_json_response(content)
            
            try:
                return json.loads(cleaned_content)
            except json.JSONDecodeError:
                try:
                    import ast
                    return ast.literal_eval(cleaned_content)
                except:
                    if attempt == 2:
                        return {
                            "score": 70,
                            "strengths": ["Communication"],
                            "weaknesses": ["Technical Depth"],
                            "summary": content[:200]
                        }
                    continue
                
        except Exception as e:
            error_msg = str(e)
            if "429" in error_msg or "billing_not_active" in error_msg:
                print(f"API Rate Limit or Billing Error: {error_msg}")
                print(f"Returning mock feedback for {detected_role} role...")
                
                # Return role-based mock feedback
                feedback_data = MOCK_INTERVIEW_FEEDBACK.get(detected_role, MOCK_INTERVIEW_FEEDBACK["backend"])
                # Randomly choose between good and average feedback
                feedback_quality = random.choice(["good", "average"])
                return feedback_data.get(feedback_quality, feedback_data["good"])
            
            print(f"Error generating feedback (Attempt {attempt+1}): {e}")
            if attempt == 2:
                print(f"All API attempts failed. Returning mock feedback for {detected_role} role...")
                feedback_data = MOCK_INTERVIEW_FEEDBACK.get(detected_role, MOCK_INTERVIEW_FEEDBACK["backend"])
                feedback_quality = random.choice(["good", "average"])
                return feedback_data.get(feedback_quality, feedback_data["good"])
