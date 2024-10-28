from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship

from database import Base

# Association table for the many-to-many relationship
student_course = Table(
    'student_course', Base.metadata,
    Column('student_id', Integer, ForeignKey('courses.id'), primary_key=True),
    Column('course_id', Integer, ForeignKey('students.id'), primary_key=True)
)


class Teacher(Base):
    __tablename__ = "teachers"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    years_of_experience = Column(Integer)

    course = relationship("Course", back_populates="teacher", cascade="all, delete, delete-orphan")


class Course(Base):
    __tablename__ = "courses"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    teacher_id = Column(Integer, ForeignKey('teachers.id'))

    teacher = relationship("Teacher", back_populates="course")
    students = relationship("Student", secondary=student_course, back_populates="courses")


class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)

    courses = relationship("Course", secondary=student_course, back_populates="students")
#Add the class below this line