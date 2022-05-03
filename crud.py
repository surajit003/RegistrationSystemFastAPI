import sqlalchemy.exc
from sqlalchemy.orm import Session

import models
import schema
from exceptions import StudentAlreadyExistException


def create_student(db: Session, student: schema.StudentCreate):
    db_item = models.Student(**student.dict())
    try:
        db.add(db_item)
        db.commit()
    except sqlalchemy.exc.IntegrityError as exc:
        raise StudentAlreadyExistException(exc.__cause__)
    db.refresh(db_item)
    return db_item


def get_students(db: Session):
    students = db.query(models.Student).all()
    return students


def get_student(db: Session, student_id: int):
    student = db.query(models.Student).get(student_id)
    return student


def filter_students_by_first_name(db: Session, first_name: str):
    # students = db.query(models.Student).filter_by(first_name=first_name)
    students = db.query(models.Student).filter(models.Student.first_name.contains(first_name))
    return students


def update_student(db: Session, student_id: int, student: schema.StudentUpdate):
    db_student = db.query(models.Student).get(student_id)
    if db_student:
        student = student.dict()
        db_student.first_name = student["first_name"]
        db_student.last_name = student["last_name"]
        db_student.email = student["email"]
        db.commit()
        db.refresh(db_student)
    return db_student


def patch_student(db: Session, student_id: int, student: schema.StudentPatch):
    db_student = db.query(models.Student).get(student_id)
    if db_student:
        student = student.dict(exclude_unset=True)
        for k, v in student.items():
            setattr(db_student, k, v)
        db.commit()
        db.refresh(db_student)
    return db_student


def delete_student(db: Session, student_id: int):
    db_student = db.query(models.Student).get(student_id)
    if db_student:
        db.delete(db_student)
        db.commit()
        return True
    else:
        return None
