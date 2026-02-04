from fastapi import FastAPI
from app.routes import employee_routes, attendance_routes
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="HRMS Lite API")

origins = [
    "http://localhost:3000", 
    "https://hrms-ui-xi.vercel.app",  
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(employee_routes.router)
app.include_router(attendance_routes.router)


@app.get("/")
def root():
    return {"message": "HRMS Lite API running"}
