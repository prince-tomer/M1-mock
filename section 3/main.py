from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import SessionLocal, engine, Base
from app import models, schemas, crud

# Create DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# DB Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ✅ Create student
@app.post("/students", response_model=schemas.StudentResponse)
def create(student: schemas.StudentCreate, db: Session = Depends(get_db)):
    return crud.create_student(db, student)

# ✅ Get all students
@app.get("/students", response_model=list[schemas.StudentResponse])
def read_students(db: Session = Depends(get_db)):
    return crud.get_students(db)

# ✅ Get one student
@app.get("/students/{student_id}", response_model=schemas.StudentResponse)
def read_student(student_id: int, db: Session = Depends(get_db)):
    student = crud.get_student(db, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

# ✅ Update student
@app.put("/students/{student_id}")
def update(student_id: int, data: schemas.StudentCreate, db: Session = Depends(get_db)):
    student = crud.update_student(db, student_id, data)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"message": "Updated successfully"}

# ✅ Delete student
@app.delete("/students/{student_id}")
def delete(student_id: int, db: Session = Depends(get_db)):
    success = crud.delete_student(db, student_id)
    if not success:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"message": "Deleted successfully"}

# 🔥 BONUS: Search by name
@app.get("/search")
def search(keyword: str = Query(...), db: Session = Depends(get_db)):
    return crud.search_students(db, keyword)