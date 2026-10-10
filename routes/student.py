from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from schemas.student import CreateStudent,StudentResponse,UpdateStudent
from models.student import Student
from database import get_db

from utility import get_current_admin

router = APIRouter(
    prefix="/student",
    tags=["Student"],
    dependencies=[Depends(get_current_admin)]
)

@router.post("/add")
def add_student(student:CreateStudent,db:Session = Depends(get_db)):

    new_student = Student(name=student.name,st_class = student.student_class, 
                          email=student.email,phone_number=student.phone_number,is_active = 
                          student.is_active
                          )

    db.add(new_student)
    db.commit()

    db.refresh(new_student)

    return{"message" :"Student Added"}

@router.get("/all")
def get_all_student(db:Session = Depends(get_db)):

    students = db.query(Student).filter().all()

    return{students}


@router.put("/update/{id}")
def update_student(id:int,student:UpdateStudent,db:Session = Depends(get_db)):

    update_student = db.query(Student).filter(Student.id == id).first()

    update_student.name=student.name,
    update_student.student_class = student.student_class, 
    update_student.email=student.email,
    update_student.phone=student.phone_number,
    update_student.is_active = student.is_active

    db.commit()

    db.refresh(update_student)

    return{"Student Updated"}

@router.delete("/delete/{id}")
def delete_student(id:int,db:Session = Depends(get_db)):

    student = db.query(Student).filter(Student.id == id).first()

    db.delete(student)

    return{"Student Deleted"}
