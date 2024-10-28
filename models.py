from sqlalchemy import Column, Integer, String
from database import Base

class Teacher(Base):
    __tablename__ = "teachers"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    years_of_experience = Column(Integer)

#Add the class below this line