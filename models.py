from sqlalchemy import Column, Integer, String, Date
from database import Base


class Employees(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)


class Timesheets(Base):
    __tablename__ = "timesheets"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer)
    work_date = Column(Date)
    amount_of_hours = Column(Integer)

