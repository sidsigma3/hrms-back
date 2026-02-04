from fastapi import APIRouter, HTTPException, Query
from app.database import attendance_collection, employee_collection
from app.schemas.attendance_schema import AttendanceCreate

router = APIRouter(prefix="/api/attendance", tags=["Attendance"])



@router.post("/")
async def mark_attendance(data: AttendanceCreate):

    employee = await employee_collection.find_one(
        {"employeeId": data.employeeId}
    )

    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    duplicate = await attendance_collection.find_one({
        "employeeId": data.employeeId,
        "date": str(data.date)
    })

    if duplicate:
        raise HTTPException(
            status_code=409,
            detail="Attendance already marked"
        )

    attendance_doc = {
        "employeeId": data.employeeId,
        "employeeName": employee["fullName"],
        "date": str(data.date),
        "status": data.status
    }

    await attendance_collection.insert_one(attendance_doc)

    
    return {"message": "Attendance marked successfully"}



@router.get("/")
async def get_all_attendance(date: str | None = Query(default=None)):

    query = {}

   
    if date:
        query["date"] = date

    records = []

    cursor = attendance_collection.find(query, {"_id": 0}).sort("date", -1)

    async for rec in cursor:
        records.append(rec)


    return records



@router.get("/{employeeId}")
async def get_attendance_by_employee(employeeId: str):

    records = []

    cursor = attendance_collection.find(
        {"employeeId": employeeId},
        {"_id": 0}
    ).sort("date", -1)

    async for rec in cursor:
        records.append(rec)


    return records
