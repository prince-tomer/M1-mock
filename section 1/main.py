# ✅ Import Libraries
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

# ✅ Data Model (Validation)
class Student(BaseModel):
    name: str
    age: int
    course: str

# ✅ In-memory database
students = {}

# ✅ GET /students → Get all students (with optional filtering)
@app.get("/students")
def get_students(course: Optional[str] = Query(None)):
    if course:
        filtered = {id: s for id, s in students.items() if s["course"].lower() == course.lower()}
        return filtered
    return students

# ✅ POST /students → Add new student
@app.post("/students", status_code=201)
def add_student(student: Student):
    student_id = len(students) + 1
    students[student_id] = student.dict()
    return {"id": student_id, "message": "Student added successfully"}

# ✅ GET /students/{id} → Get specific student
@app.get("/students/{student_id}")
def get_student(student_id: int):
    if student_id not in students:
        raise HTTPException(status_code=404, detail="Student not found")
    return students[student_id]

# ✅ PUT /students/{id} → Update student
@app.put("/students/{student_id}")
def update_student(student_id: int, updated_student: Student):
    if student_id not in students:
        raise HTTPException(status_code=404, detail="Student not found")
    students[student_id] = updated_student.dict()
    return {"message": "Student updated successfully"}

# ✅ DELETE /students/{id} → Delete student
@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    if student_id not in students:
        raise HTTPException(status_code=404, detail="Student not found")
    del students[student_id]
    return {"message": "Student deleted successfully"}
