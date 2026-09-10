from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi import Depends
from sqlalchemy.orm import Session
from sqlalchemy import select
engine = create_engine("sqlite:///students.db")
app = FastAPI()
SessionLocal  = sessionmaker(bind = engine)
db = SessionLocal()
def get_db():
      db = SessionLocal()
      try:
            yield db
      finally:
              db.close()
class Base(DeclarativeBase):
      pass
class Student(Base):
      id : Mapped[int] = mapped_column(primary_key = True)
      name : Mapped[str] = mapped_column()
      age : Mapped[int] = mapped_column()
      __tablename__ = "students"
class StudentCreate(BaseModel):
            name: str
            age : int
Base.metadata.create_all(engine)
students = []
@app.get("/students")
def read_student(db: Session = Depends(get_db)):
    stmt = select(Student)
    result = db.execute(stmt)
    students = result.scalars().all()
    return students

class Student_details(BaseModel):
           id : int
           name : str
           age : int
@app.delete("/students/{student_id}")
def delete_student(student_id : int):
     for student in students:
          if student["id"] == student_id:
             students.remove(student)
             return student
     raise HTTPException(status_code = 404, detail = "id not found")

@app.put("/students/{student_id}")
def update_students(student_id : int , student_details : Student_details):
     for student in students:
           if student["id"] == student_id:
                student["name"] = student_details.name
                student["age"] = student_details.age
                return student
     raise HTTPException(status_code = 404, detail = "id not found")
class Student_patch(BaseModel):
           name : str | None = None
           age : int | None = None
@app.patch("/students/{student_id}")
def patch_student(student_id : int , student_details : Student_patch ):
     for student in students:
          if student["id"] == student_id:
               if student_details.name is not None:
                    student["name"] = student_details.name
               if student_details.age is not None: 
                    student["age"] = student_details.age
          return student
     raise HTTPException(status_code = 404, detail = "id not found")
