from typing import Optional

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import engine, Base, get_db
from models import Teacher, Course, Student
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


@app.post("/teachers/{teacher_id}/courses/")
def create_course(teacher_id: int, title: str, description: str, db: Session = Depends(get_db)):
    db_course = Course(title=title, description=description, teacher_id=teacher_id)
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return jsonable_encoder(db_course)


@app.post("/students/")
def create_student(first_name: str, last_name: str, db: Session = Depends(get_db)):
    db_student = Student(first_name=first_name, last_name=last_name)
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return jsonable_encoder(db_student)


# Read a Teacher by ID
@app.get("/teachers/{teacher_id}")
def read_teacher(teacher_id: int, db: Session = Depends(get_db)):
    db_teacher = db.query(Teacher).filter(Teacher.id == teacher_id).first()
    if db_teacher is None:
        raise HTTPException(status_code=404, detail="Teacher not found")
    return jsonable_encoder(db_teacher)


# Read a Course by Teacher ID
@app.get("/teachers/{teacher_id}/courses/")
def read_courses_by_teacher(teacher_id: int, db: Session = Depends(get_db)):
    db_course = db.query(Course).filter(Course.teacher_id == teacher_id)
    if db_course is None:
        raise HTTPException(status_code=404, detail="Courses for this teacher not found")
    return jsonable_encoder(db_course)


@app.get("/courses/{course_id}")
def read_course(course_id: int, db: Session = Depends(get_db)):
    db_course = db.query(Course).filter(Course.id == course_id).first()
    if db_course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    return jsonable_encoder(db_course)


@app.get("/students/{student_id}")
def read_student(student_id: int, db: Session = Depends(get_db)):
    db_student = db.query(Student).filter(Student.id == student_id).first()
    if db_student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return jsonable_encoder(db_student)


@app.get("/courses/{course_id}/teacher")
def read_teacher_from_course(course_id: int, db: Session = Depends(get_db)):
    db_course = db.query(Course).filter(Course.id == course_id).first()
    if db_course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    db_teacher = db_course.teacher

    return jsonable_encoder(db_teacher)


@app.get("/courses/{course_id}/students")
def read_students_from_course(course_id: int, db: Session = Depends(get_db)):
    db_course = db.query(Course).filter(Course.id == course_id).first()
    if db_course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    db_students = db_course.students

    return jsonable_encoder(db_students)


@app.get("/students/{student_id}/courses")
def read_courses_for_student(student_id: int, db: Session = Depends(get_db)):
    db_student = db.query(Student).filter(Student.id == student_id).first()
    if db_student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    db_courses = db_student.courses

    return jsonable_encoder(db_courses)


# Read All Teachers
@app.get("/teachers/")
def read_teachers(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    teachers = db.query(Teacher).offset(skip).limit(limit).all()
    return jsonable_encoder(teachers)


@app.get("/courses/")
def read_courses(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    courses = db.query(Course).offset(skip).limit(limit).all()
    return jsonable_encoder(courses)


@app.get("/students/")
def read_courses(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    courses = db.query(Student).offset(skip).limit(limit).all()
    return jsonable_encoder(courses)


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


@app.put("/students/{student_id}")
def update_teacher(student_id: int, first_name: Optional[str] = None, last_name: Optional[str] = None,
                    db: Session = Depends(get_db)):
    db_student = db.query(Student).filter(Student.id == student_id).first()
    if db_student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    if first_name is not None:
        db_student.first_name = first_name
    if last_name is not None:
        db_student.last_name = last_name
    db.commit()
    db.refresh(db_student)
    return jsonable_encoder(db_student)


@app.put("/courses/{course_id}")
def update_course(course_id: int, title: Optional[str] = None, description: Optional[str] = None,
                    db: Session = Depends(get_db)):
    db_course = db.query(Course).filter(Course.id == course_id).first()
    if db_course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    if title is not None:
        db_course.title = title
    if description is not None:
        db_course.description = description
    db.commit()
    db.refresh(db_course)
    return jsonable_encoder(db_course)


@app.put("/courses/{course_id}/{student_id}")
def associate_students_with_course(course_id: int, student_id: int, db: Session = Depends(get_db)):
    db_course = db.query(Course).filter(Course.id == course_id).first()
    if db_course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    db_student = db.query(Student).filter(Student.id == student_id).first()
    if db_student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    db_course.students.append(db_student)
    db.commit()
    db.refresh(db_course)
    return jsonable_encoder(db_course)


# Delete a Teacher
@app.delete("/teachers/{teacher_id}")
def delete_teacher(teacher_id: int, db: Session = Depends(get_db)):
    db_teacher = db.query(Teacher).filter(Teacher.id == teacher_id).first()
    if db_teacher is None:
        raise HTTPException(status_code=404, detail="Teacher not found")
    db.delete(db_teacher)
    db.commit()
    return {"message": f"Teacher with ID {teacher_id} deleted successfully"}


@app.delete("/students/{student_id}")
def delete_teacher(student_id: int, db: Session = Depends(get_db)):
    db_student = db.query(Student).filter(Student.id == student_id).first()
    if db_student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    db.delete(db_student)
    db.commit()
    return {"message": f"Student with ID {db_student} deleted successfully"}


@app.delete("/courses/{course_id}")
def delete_course(course_id: int, db: Session = Depends(get_db)):
    db_course = db.query(Course).filter(Course.id == course_id).first()
    if db_course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    db.delete(db_course)
    db.commit()
    return {"message": f"Course with ID {course_id} deleted successfully"}

#Add new endpoints below this line
