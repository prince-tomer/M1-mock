from sqlalchemy.orm import Session
from app import models

# Create
def create_student(db: Session, student):
    db_student = models.Student(**student.dict())
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

# Get all
def get_students(db: Session):
    return db.query(models.Student).all()

# Get one
def get_student(db: Session, student_id: int):
    return db.query(models.Student).filter(models.Student.id == student_id).first()

# Update
def update_student(db: Session, student_id: int, data):
    student = get_student(db, student_id)
    if student:
        student.name = data.name
        student.age = data.age
        student.course = data.course
        db.commit()
        return student
    return None

# Delete
def delete_student(db: Session, student_id: int):
    student = get_student(db, student_id)
    if student:
        db.delete(student)
        db.commit()
        return True
    return False

# 🔥 Bonus: Search by name
def search_students(db: Session, keyword: str):
    return db.query(models.Student).filter(models.Student.name.contains(keyword)).all()