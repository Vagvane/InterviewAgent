from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings

app = FastAPI(title="Interview Agent API", version="1.0.0")

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from fastapi.middleware.gzip import GZipMiddleware
app.add_middleware(GZipMiddleware, minimum_size=1000)

@app.get("/")
def read_root():
    return {"message": "Welcome to Interview Agent API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

from app.api import auth, users, assessment, coding, interview, profile
app.include_router(auth.router, prefix=f"{settings.API_V1_STR}", tags=["login"])
app.include_router(users.router, prefix=f"{settings.API_V1_STR}/users", tags=["users"])
app.include_router(assessment.router, prefix=f"{settings.API_V1_STR}/assessment", tags=["assessment"])
app.include_router(coding.router, prefix=f"{settings.API_V1_STR}/coding", tags=["coding"])
app.include_router(interview.router, prefix=f"{settings.API_V1_STR}/interview", tags=["interview"])
app.include_router(profile.router, prefix=f"{settings.API_V1_STR}/profile", tags=["profile"])

# Create tables on startup (for simple local dev)
from app.db.session import engine
from app.db.base_class import Base
Base.metadata.create_all(bind=engine)

