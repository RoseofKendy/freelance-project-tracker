# database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base # Import Base from models.py

DATABASE_URL = "sqlite:///freelance_tracker.db"

# Create a SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """
    Initializes the database.
    With Alembic, we no longer call Base.metadata.create_all() here.
    Alembic migrations will handle schema creation and updates.
    This function can now be empty or used for other initial setup if needed.
    """
    # Base.metadata.create_all(bind=engine) # REMOVE OR COMMENT OUT THIS LINE
    print(f"Database engine created for {DATABASE_URL}")


def get_db():
    """
    Dependency to get a database session.
    This function yields a session and ensures it's closed after use.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

if __name__ == "__main__":
    
    init_db()
