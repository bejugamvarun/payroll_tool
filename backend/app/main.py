from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.routers import (
    colleges,
    departments,
    employees,
    salary_components,
    leave_policies,
    attendance,
    holidays,
    payroll,
    payslips,
    reports,
)

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Aurora Group Payroll Management System API"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=settings.CORS_ALLOW_METHODS,
    allow_headers=settings.CORS_ALLOW_HEADERS,
)


# Health check endpoint
@app.get("/")
def root():
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running"
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}


# Include routers
app.include_router(colleges.router, prefix="/api/v1")
app.include_router(departments.router, prefix="/api/v1")
app.include_router(employees.router, prefix="/api/v1")
app.include_router(salary_components.router, prefix="/api/v1")
app.include_router(leave_policies.router, prefix="/api/v1")
app.include_router(attendance.router, prefix="/api/v1")
app.include_router(holidays.router, prefix="/api/v1")
app.include_router(payroll.router, prefix="/api/v1")
app.include_router(payslips.router, prefix="/api/v1")
app.include_router(reports.router, prefix="/api/v1")
