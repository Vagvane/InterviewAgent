# Interview Agent

A full-stack AI-powered Interview Agent application built with FastAPI (Backend) and Next.js (Frontend).

## Features
- **User Authentication**: Login and Signup.
- **Daily Assessment**: AI-generated technical questions (MCQ/Subjective).
- **Coding Arena**: Integrated Monaco Editor for solving coding problems.
- **AI Interview**: Interactive video/chat interview with an AI avatar.
- **Profile & Analytics**: Detailed statistics and skills analysis.

## Setup Instructions

### Prerequisites
- Node.js (v18+)
- Python (v3.9+)
- PostgreSQL (Optional, defaults to SQLite)

### Backend Setup
1. Navigate to the `backend` directory:
   ```bash
   cd backend
   ```
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the server:
   ```bash
   uvicorn app.main:app --reload
   ```
   The API will be available at `http://localhost:8000`.

### Frontend Setup
1. Navigate to the `frontend` directory:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Run the development server:
   ```bash
   npm run dev
   ```
   The app will be available at `http://localhost:3000`.

## Configuration
- **Backend**: Update `backend/app/core/config.py` or create a `.env` file for API keys (OpenAI) and Database URL.
- **Frontend**: API URL is configured in `frontend/lib/api.ts`.
