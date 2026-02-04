from pydantic import BaseModel
from datetime import date
from typing import Literal

class AttendanceCreate(BaseModel):
    employeeId: str
    date: date
    status: Literal["Present", "Absent"]
