from fastapi    import FastAPI, HTTPException, Depends
from pydantic   import BaseModel
from sqlalchemy import create_engine,select
from sqlalchemy.orm import DeclarativeBase,Mapped,mapped_column,Session,sessionmaker

app = FastAPI()

class Base(DeclarativeBase):
      pass
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

engine = create_engine("sqlite:///students.db")
Base.metadata.create_all(engine)
SessionLocal = sessionmaker(bind = engine)
def get_db():
    db = SessionLocal()
    try:
         yield db
    finally:
            db.close()
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