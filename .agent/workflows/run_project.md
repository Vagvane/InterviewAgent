---
description: How to run the Interview Agent project (Backend & Frontend)
---

This workflow describes how to start both the FastAPI backend and the Next.js frontend.

## Prerequisites
- Python 3.10+
- Node.js 18+
- PostgreSQL (optional, defaults to SQLite)

## 1. Start the Backend Server

Open a new terminal and run:

```powershell
cd backend
# Activate Virtual Environment
.\venv\Scripts\Activate.ps1
# Start FastAPI Server
uvicorn app.main:app --reload
```

The backend will start at `http://localhost:8000`.
API Documentation is available at `http://localhost:8000/docs`.

## 2. Start the Frontend Server

Open a **separate** terminal and run:

```powershell
cd frontend
# Start Next.js Dev Server
npm run dev
```

The frontend will start at `http://localhost:3000`.

## Troubleshooting

- **Backend Port in Use**: If port 8000 is busy, `uvicorn` will fail. Kill the process using that port or specify a different one: `uvicorn app.main:app --reload --port 8001`.
- **Frontend Port in Use**: Next.js will automatically try port 3001 if 3000 is taken.
- **Environment Variables**: Ensure `backend/.env` is properly configured.
