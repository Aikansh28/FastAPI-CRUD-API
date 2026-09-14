from fastapi    import FastAPI, HTTPException, Depends
from pydantic   import BaseModel
from sqlalchemy import create_engine,select
from sqlalchemy.orm import DeclarativeBase,Mapped,mapped_column,Session,sessionmaker
from database import Base,get_db
app = FastAPI()

class Student(Base):
      __tablename__ = "students"
      id : Mapped[int] = mapped_column(primary_key = True)
      name : Mapped[str] = mapped_column()
      age : Mapped[int] = mapped_column()

class StudentPost(BaseModel):
      name : str
      age : int
class StudentPatch(BaseModel):
      name : str | None = None
      age  : int | None = None 

class ResponseModel(BaseModel):
      id : int
      name: str
      age : int 

@app.get("/students/{student_id}")
def get_students(student_id : int , db: Session = Depends(get_db)):
    stmt = select(Student).where(Student.id == student_id)
    result = db.execute(stmt)
    student = result.scalar_one_or_none()
    if student is None:
       raise HTTPException(status_code =404 , detail = " student does not exist")
    return student
@app.post("/students" , response_model = ResponseModel)
def post_students(student_details: StudentPost, db: Session = Depends(get_db)):
    student = Student(name = student_details.name , age = student_details.age)
    db.add(student)
    db.commit()
    db.refresh(student)
    return student
@app.put("/students/{student_id}")
def put_students(student_id : int, student_details : StudentPost, db: Session = Depends(get_db)):
    stmt = select(Student).where(Student.id == student_id)
    result = db.execute(stmt)
    student = result.scalar_one_or_none()
    if student is None:
       raise HTTPException(status_code = 404 ,detail = "student does not exist")
    student.name = student_details.name
    student.age = student_details.age
    db.commit()
    return student
@app.patch("/students/{student_id}")
def patch_students(student_id : int, student_details: StudentPatch ,db: Session = Depends(get_db)):
    stmt = select(Student).where(Student.id == student_id)
    result = db.execute(stmt)
    student = result.scalar_one_or_none()
    if student is None:
       raise  HTTPException(status_code = 404 , detail = "student does not exist") 
    if student_details.name is not None:
       student.name = student_details.name 
    if student_details.age is not None:
       student.age = student_details.age
    db.commit()
    return student
@app.delete("/students/{student_id}")
def delete_students(student_id : int , db: Session = Depends(get_db)):
    stmt = select(Student).where(Student.id == student_id)
    result = db.execute(stmt)
    student = result.scalar_one_or_none()
    if student is None:
       raise HTTPException(status_code= 404, detail = "student does not exist")
    db.delete(student)
    db.commit()
    return student