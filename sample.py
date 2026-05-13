from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

@app.get("/")

#Path parameters — part of the URL
#A path param is a variable piece of the URL. You use it to identify which specific item you want. Think of it like this:
#Real-world analogy: Imagine a library. The URL is like the shelf location:

# Without path param — get ALL books
#GET /books

# With path param — get book number 5 specifically
#GET /books/5

# Another path param — get chapter 3 of book 5
#GET /books/5/chapters/3

# Step 1: put {id} in the route path
@app.get("/students/${id}")

def root():
    return {"message": "Hello from FastAPI!"}

# Step 2: add same name as function param with a type
def getStudent(id:int):
        return {"id":id}

# When someone calls: GET /students/42
# FastAPI puts 42 into the id variable
# → {"student_id": 42}


@app.get("classes/{class_id}/students/{students_id}")
def get_students(class_id:int,student_id:int):
      return{
            "class":class_id,
            "student":student_id
      }


#Query parameters — filters after the ?
#🔍 Real-world analogy: Query params are like search filters on a shopping website. You go to the same page (/products) but filter what you see:

# Same endpoint — different results based on filters
#GET /products?category=shoes
#GET /products?category=shoes&size=42&color=black
#GET /students?skip=0&limit=10
#GET /students?search=kailas
#

#How to write it in FastAPI
#Any function parameter that is NOT in the URL path → FastAPI treats it as a query param. That simple.
## Optional query param — may or may not be sent

def list_students(skip:int=0,limit:int=0,search: Optional[str] = None):
      if search:
            return {"searching for":search}
      return {"skip":skip,"limit":limit}
# GET /students           → skip=0, limit=10  (defaults)
# GET /students?skip=5   → skip=5, limit=10
# GET /students?skip=5&limit=20 → skip=5, limit=20




#Request body — data sent invisibly with the request
#📦 Real-world analogy: Path and query params are like writing on the outside of an envelope (the address). The request body is like the letter inside the envelope — hidden, 
# can be big, and is what you're actually sending.

# You can't put a whole student object in the URL
# ✗ This is ugly and limited:
#GET /students?name=Kailas&age=28&email=k@test.com&grade=9.5

# ✓ Send it as body — clean and unlimited:
#POST /students
#{
#    "name":  "Kailas",
#   "age":   28,
#  "email": "k@test.com",
#   "grade": 9.5
#}

#How to write it in FastAPI — Pydantic model
#First define the shape of the data (called a model), then use it as a function param:

# Step 1 — Define the shape of your data
class Student(BaseModel): #like blur print
      name:str
      age:int
      email:str = None #optional
      
# Step 2 — Use the model as a function param
def create_student(student: Student):
# FastAPI sees "Student" model → expects JSON body
    return {
        "message": "Student created!",
        "name":    student.name,
        "age":     student.age
    }


# What you send (in /docs or Postman):
{
    "name": "Kailas",
    "age":  28
}

# What you get back:
{
    "message": "Student created!",
    "name":    "Kailas",
    "age":     28
}

# PUT /students/42  + body = update student 42
@app.put("/students/{id}")
def update_student(id:int,student:Student):
      return {"updated id":id,"data":student.name}

# URL:  PUT /students/42
# Body: {"name":"Kailas Updated","age":29}
# FastAPI knows: 42 = path, {name,age} = body

#create db
students_db = []

