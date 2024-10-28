from typing import Optional

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import engine, Base, get_db
from models import Teacher
from fastapi.encoders import jsonable_encoder

app = FastAPI()

# Create database tables
Base.metadata.create_all(bind=engine)


# Create a Teacher
@app.post("/teachers/")
def create_teacher(first_name: str, last_name: str, years_of_experience: int, db: Session = Depends(get_db)):
    db_teacher = Teacher(first_name=first_name, last_name=last_name, years_of_experience=years_of_experience)
    db.add(db_teacher)
    db.commit()
    db.refresh(db_teacher)
    return jsonable_encoder(db_teacher)


# Read a Teacher by ID
@app.get("/teachers/{teacher_id}")
def read_teacher(teacher_id: int, db: Session = Depends(get_db)):
    db_teacher = db.query(Teacher).filter(Teacher.id == teacher_id).first()
    if db_teacher is None:
        raise HTTPException(status_code=404, detail="Teacher not found")
    return jsonable_encoder(db_teacher)


# Read All Teachers
@app.get("/teachers/")
def read_teachers(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    teachers = db.query(Teacher).offset(skip).limit(limit).all()
    return jsonable_encoder(teachers)


# Update a Teacher
@app.put("/teachers/{teacher_id}")
def update_teacher(teacher_id: int, first_name: Optional[str] = None, last_name: Optional[str] = None,
                   years_of_experience: Optional[int] = None, db: Session = Depends(get_db)):
    db_teacher = db.query(Teacher).filter(Teacher.id == teacher_id).first()
    if db_teacher is None:
        raise HTTPException(status_code=404, detail="Teacher not found")
    if first_name is not None:
        db_teacher.first_name = first_name
    if last_name is not None:
        db_teacher.last_name = last_name
    if years_of_experience is not None:
        db_teacher.years_of_experience = years_of_experience
    db.commit()
    db.refresh(db_teacher)
    return jsonable_encoder(db_teacher)


# Delete a Teacher
@app.delete("/teachers/{teacher_id}")
def delete_teacher(teacher_id: int, db: Session = Depends(get_db)):
    db_teacher = db.query(Teacher).filter(Teacher.id == teacher_id).first()
    if db_teacher is None:
        raise HTTPException(status_code=404, detail="Teacher not found")
    db.delete(db_teacher)
    db.commit()
    return {"message": f"Teacher with ID {teacher_id} deleted successfully"}

#Add new endpoints below this line
