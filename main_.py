from fastapi import FastAPI,HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List

app = FastAPI(title="Student API", version="1.0.0")


#------------------Model----------------------
class Student(BaseModel):
    name :str   = Field(min_length=2)
    age: int    = Field(gt=0, le=100)
    grade: float    = Field(gt=0.0, le=10.0)
    email : Optional[str] = None

#----------------In-Memory Store--------------
students_db: List[dict] = [] #our fake db
next_id =1  #auto increment counter

#-----------------Helper- find student or raise 404------------
def find_student(student_id:int):
    for s in students_db:
        if s["id"] == student_id:
            return student_id
    raise HTTPException(status_code=404,detail=f"Student {student_id} not found")


#----------------Create--POST/Students-------------------------
@app.post("/students",status_code=201)
def create_student(student:Student):
    global next_id
    data = student.model_dump() #convert model->dict
    data["id"] = next_id
    next_id +=1
    students_db.append(data)
    return data

# ── READ ALL ── GET /students ──────────────────────────
@app.get("/students")
def get_all_students():
    return students_db

# ── READ ONE ── GET /students/{id} ────────────────────
@app.get("/students/{student_id}")
def get_student(student_id:int):
    return find_student(student_id)

# ── UPDATE ── PUT /students/{id} ──────────────────────
def update_student(student_id: int, student: Student):
    existing = find_student(student_id)   # 404 if not found
    updated  = student.model_dump()
    updated["id"] = student_id
    idx = students_db.index(existing)
    students_db[idx] = updated
    return updated

# ── DELETE ── DELETE /students/{id} ───────────────────
@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    student = find_student(student_id)    # 404 if not found
    students_db.remove(student)
    return {"message": f"Student {student_id} deleted"}





