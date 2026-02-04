from fastapi import APIRouter, HTTPException
from app.database import employee_collection, attendance_collection
from app.schemas.employee_schema import EmployeeCreate

router = APIRouter(prefix="/api/employees", tags=["Employees"])



@router.post("/")
async def create_employee(employee: EmployeeCreate):

    existing = await employee_collection.find_one({
        "$or": [
            {"employeeId": employee.employeeId},
            {"email": employee.email}
        ]
    })

    if existing:
        raise HTTPException(status_code=409, detail="Employee already exists")

    await employee_collection.insert_one(employee.dict())

    return {"message": "Employee created successfully"}
    


@router.get("/")
async def get_employees():

    employees = []
    cursor = employee_collection.find()

    async for emp in cursor:
        emp["_id"] = str(emp["_id"])
        employees.append(emp)

    return employees



@router.delete("/{employee_id}")
async def delete_employee(employee_id: str):

    result = await employee_collection.delete_one({"employeeId": employee_id})

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Employee not found")

    
    await attendance_collection.delete_many({"employeeId": employee_id})

    return {"message": "Employee deleted"}
