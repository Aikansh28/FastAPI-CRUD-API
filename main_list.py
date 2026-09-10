from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()
students = []
class Student(BaseModel):
      id  : int
      name : str
      age : int
class StudentPost(BaseModel):
      name : str
      age    : int     
class StudentPatch(BaseModel):
      name : str | None = None
      age  : int | None = None
class Response_model(BaseModel):
      id : int
      name : str
      age : int

@app.get("/students/{student_id}")
def get_students(student_id : int):
    for student in students:
        if student.id == student_id:
           return student
    raise HTTPException(status_code = 404, detail = "student does not exist")

@app.post("/students" , response_model = Response_model )
def post_student(student_details: StudentPost):
    if students:
       new_id = students[-1].id +1
    else:
         new_id = 1
    student = Student(
         id = new_id,
         name = student_details.name,
         age = student_details.age
         )
    students.append(student)
    return student

@app.put("/students/{student_id}")
def put_students(student_id : int , student_details : Student):
    for student in students:
        if student_id == student.id:
           student.name = student_details.name 
           student.age = student_details.age
           return student
    raise HTTPException(status_code= 404, detail = "student does not exist")

@app.patch("/students/{student_id}")
def patch_students(student_id : int , student_details : StudentPatch):
    for student in students:
        if student_id == student.id:
           if student_details.name is not None:
              student.name = student_details.name 
           if student_details.age is not None :
               student.age = student_details.age
           return student
    raise HTTPException(status_code= 404, detail ="student does not exist")
@app.delete("/students/{student_id}")
def delete_students(student_id : int):
    for student in students:
        if student_id == student.id:
           students.remove(student)
           return student
    raise HTTPException(status_code= 404, detail ="student does not exist")





    
