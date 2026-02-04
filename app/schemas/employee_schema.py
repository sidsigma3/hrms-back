from pydantic import BaseModel, EmailStr

class EmployeeCreate(BaseModel):
    employeeId: str
    fullName: str
    email: EmailStr
    department: str
