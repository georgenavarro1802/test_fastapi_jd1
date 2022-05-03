from datetime import date
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import Optional

from sqlalchemy import and_

from database import engine, SessionLocal
from sqlalchemy.orm import Session
from models import Base, Employees, Timesheets

app = FastAPI()

Base.metadata.create_all(bind=engine)


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


class Employee(BaseModel):
    name: str = Field(min_length=1)


class Timesheet(BaseModel):
    employee_id: int = Field(gt=0)
    work_date: Optional[date] = None
    amount_of_hours: int = Field(gt=0)


# # # Employees - Endpoints # # #
@app.get("/employees")
def all_employees(db: Session = Depends(get_db)):
    """
    Return a list with all the employees
    """
    return db.query(Employees).all()


@app.post("/employees")
def create_employee(employee: Employee, db: Session = Depends(get_db)):
    """
    Create an employee
    """

    employee_model = Employees()
    employee_model.name = employee.name

    db.add(employee_model)
    db.commit()

    return employee


@app.put("/employees/{id}")
def update_employee(employee_id: int, employee: Employee, db: Session = Depends(get_db)):
    """
    Update an employee
    """
    employee_model = db.query(Employees).filter(Employees.id == employee_id).first()

    if employee_model is None:
        raise HTTPException(
            status_code=404,
            detail=f"ID {employee_id} : Does not exist"
        )

    employee_model.name = employee.name

    db.add(employee_model)
    db.commit()

    return employee


@app.delete("/employees/{id}")
def delete_employee(employee_id: int, db: Session = Depends(get_db)):
    """
    Delete an employee
    """
    employee_model = db.query(Employees).filter(Employees.id == employee_id).first()

    if employee_model is None:
        raise HTTPException(
            status_code=404,
            detail=f"ID {employee_id} : Does not exist"
        )

    db.query(Employees).filter(Employees.id == employee_id).delete()

    db.commit()


# # # Timesheets - Endpoints # # #
@app.get("/timesheets")
def timesheets(employee_id: Optional[int] = None, work_date: Optional[date] = None, db: Session = Depends(get_db)):
    """
    List all the timesheets or if employee_id and date are passed as parameters it will return the timesheets records related to the employee and its date
    :return:
    """
    if employee_id and work_date:
        return db.query(Timesheets).filter(and_(Timesheets.employee_id == employee_id, Timesheets.work_date == work_date)).first()
    return db.query(Timesheets).all()


@app.post("/timesheets")
def create_timesheet(timesheet: Timesheet, db: Session = Depends(get_db)):
    """
    Create a Timesheet
    """
    timesheet_model = Timesheets()
    timesheet_model.employee_id = timesheet.employee_id
    timesheet_model.work_date = timesheet.work_date
    timesheet_model.amount_of_hours = timesheet.amount_of_hours

    db.add(timesheet_model)
    db.commit()

    return timesheet
