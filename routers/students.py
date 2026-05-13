from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
import models, schemas
from database import get_db

router = APIRouter()

# CREATE
@router.post("/", response_model=schemas.StudentResponse, status_code=201)
def create_student(student: schemas.StudentCreate, db: Session = Depends(get_db)):
    db_student = models.Student(**student.model_dump())
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

# READ ALL
@router.get("/", response_model=List[schemas.StudentResponse])
def get_all(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(models.Student).offset(skip).limit(limit).all()

# READ ONE
@router.get("/{student_id}", response_model=schemas.StudentResponse)
def get_one(student_id: int, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(
        models.Student.id == student_id
    ).first()
    if not student:
        raise HTTPException(404, "Student not found")
    return student

# UPDATE
@router.put("/{student_id}", response_model=schemas.StudentResponse)
def update(student_id: int, student: schemas.StudentCreate, db: Session = Depends(get_db)):
    db_s = db.query(models.Student).filter(
        models.Student.id == student_id
    ).first()
    if not db_s:
        raise HTTPException(404, "Student not found")
    for k, v in student.model_dump().items():
        setattr(db_s, k, v)
    db.commit()
    db.refresh(db_s)
    return db_s

# DELETE
@router.delete("/{student_id}")
def delete(student_id: int, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(
        models.Student.id == student_id
    ).first()
    if not student:
        raise HTTPException(404, "Student not found")
    db.delete(student)
    db.commit()
    return {"message": f"Student {student_id} deleted"}