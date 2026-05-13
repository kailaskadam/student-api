from sqlalchemy import Column,Integer,Float,String,Boolean
from database import Base


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer,primary_key=True,index=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    grade = Column(Float , default=0.0)
    email = Column(String, nullable=False)
    active = Column(Boolean , default=True)

# This creates this table in PostgreSQL:
# CREATE TABLE students (
#   id     SERIAL PRIMARY KEY,
#   name   VARCHAR NOT NULL,
#   age    INTEGER NOT NULL,
#   grade  FLOAT DEFAULT 0.0,
#   email  VARCHAR,
#   active BOOLEAN DEFAULT TRUE
# );