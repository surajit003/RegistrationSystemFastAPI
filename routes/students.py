from fastapi import APIRouter
from fastapi import Depends, status, HTTPException

from sqlalchemy.orm import Session

import exceptions
import schema
import crud
from dependencies.dependencies import get_db
import utils

router = APIRouter(
    prefix="/students",
    tags=["students"],
    responses={404: {"description": "Not found"}},
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_item(student: schema.StudentCreate, db: Session = Depends(get_db)):
    try:
        student = crud.create_student(db=db, student=student)
    except exceptions.StudentAlreadyExistException as exc:
        raise HTTPException(status_code=200, detail=str(exc))
    return student


@router.get("/", status_code=status.HTTP_200_OK)
def get_students(db: Session = Depends(get_db)):
    students = crud.get_students(db)
    return students


@router.get("/{student_id}", status_code=status.HTTP_200_OK)
def get_student(student_id: int, db: Session = Depends(get_db)):
    student = crud.get_student(db, student_id)
    return student


@router.get("/first_name/{first_name}", status_code=status.HTTP_200_OK)
def get_students_by_first_name(first_name: str, db: Session = Depends(get_db)):
    students = crud.filter_students_by_first_name(db, first_name)
    return utils.convert_to_dict(students)


@router.put("/{student_id}", status_code=status.HTTP_200_OK)
def update_student(
    student_id: int, student: schema.StudentUpdate, db: Session = Depends(get_db)
):
    student = crud.update_student(db, student_id, student)
    if not student:
        raise HTTPException(
            status_code=404, detail=f"Student with id {student_id} not found"
        )
    return student


@router.patch("/{student_id}", status_code=status.HTTP_200_OK)
def patch_student(
    student_id: int, student: schema.StudentPatch, db: Session = Depends(get_db)
):
    student = crud.patch_student(db, student_id, student)
    if not student:
        raise HTTPException(
            status_code=404, detail=f"Student with id {student_id} not found"
        )
    return student


@router.delete("/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_student(student_id: int, db: Session = Depends(get_db)):
    student = crud.delete_student(db, student_id)
    if student is None:
        raise HTTPException(
            status_code=404, detail=f"Student with id {student_id} not found"
        )
    return student
