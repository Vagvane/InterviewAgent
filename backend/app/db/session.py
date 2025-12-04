from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Use SQLite for local development if Postgres is not set up, or just use the string
# For now, let's assume SQLite for simplicity if the user hasn't provided a real DB URL, 
# but the plan said Postgres. I'll stick to the config.
# However, to make it run immediately without external DB setup, SQLite is safer.
# But the user asked for a full project. I will use SQLite as default in config if not provided.
# Let's update config to use sqlite by default for ease of run.

SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL
if "sqlite" in SQLALCHEMY_DATABASE_URL:
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    )
else:
    engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
