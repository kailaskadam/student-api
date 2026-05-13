from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,DeclarativeBase

# 1. Connection string — change to your credentials
DATABASE_URL = "postgresql://postgres:password@localhost:5432/student_db"

# 2. Engine — the actual connection to PostgreSQL
engine = create_engine(DATABASE_URL)

# 3.SessionLocal — a factory that creates DB sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4.Base — all SQLAlchemy models inherit from this
class Base(DeclarativeBase):
    pass

# 5. get_db — opens/closes session for each request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()