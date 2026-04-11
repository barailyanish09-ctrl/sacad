from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base

# ── Change this to PostgreSQL URL when deploying to production ──
DATABASE_URL = "sqlite:///./sacad.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """Create all tables if they don't exist."""
    Base.metadata.create_all(bind=engine)

def get_db():
    """FastAPI dependency — yields a DB session per request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()