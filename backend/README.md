# Aurora Group Payroll Management System - Backend

This is the backend API for the Aurora Group Payroll Management System, built with FastAPI, PostgreSQL, and SQLAlchemy.

## Features

- College and employee management with bulk operations
- Department and designation management
- Salary component configuration
- Leave policy and balance tracking
- Attendance upload and processing from Excel files
- Holiday management
- Automated payroll calculation
- Payslip PDF generation
- Comprehensive reporting system

## Technology Stack

- **Framework**: FastAPI 0.109.0
- **Database**: PostgreSQL 15
- **ORM**: SQLAlchemy 2.0.25
- **Migrations**: Alembic 1.13.1
- **Excel Processing**: openpyxl, pandas
- **PDF Generation**: reportlab
- **Authentication**: python-jose, passlib (for future implementation)

## Project Structure

```
backend/
├── alembic/                    # Database migrations
│   ├── versions/              # Migration files
│   ├── env.py                 # Alembic environment
│   └── script.py.mako         # Migration template
├── app/
│   ├── models/                # SQLAlchemy ORM models
│   │   ├── colleges.py
│   │   ├── departments.py
│   │   ├── designations.py
│   │   ├── salary_components.py
│   │   ├── employees.py
│   │   ├── employee_salary_structures.py
│   │   ├── leave_policies.py
│   │   ├── employee_leave_balances.py
│   │   ├── attendance_uploads.py
│   │   ├── attendance_records.py
│   │   ├── holidays.py
│   │   ├── payroll_cycles.py
│   │   ├── payroll_entries.py
│   │   ├── payroll_entry_components.py
│   │   ├── payslips.py
│   │   └── reports.py
│   ├── routers/               # API endpoints
│   │   ├── colleges.py
│   │   ├── departments.py
│   │   ├── employees.py
│   │   ├── salary_components.py
│   │   ├── leave_policies.py
│   │   ├── attendance.py
│   │   ├── holidays.py
│   │   ├── payroll.py
│   │   ├── payslips.py
│   │   └── reports.py
│   ├── schemas/               # Pydantic schemas
│   ├── services/              # Business logic
│   ├── repositories/          # Data access layer
│   ├── utils/                 # Utilities
│   ├── config.py              # Configuration
│   ├── database.py            # Database setup
│   └── main.py                # FastAPI app
├── storage/                   # File storage
│   ├── uploads/              # Uploaded attendance files
│   ├── payslips/             # Generated payslips
│   └── reports/              # Generated reports
├── Dockerfile
├── requirements.txt
└── alembic.ini
```

## Setup Instructions

### 1. Using Docker (Recommended)

```bash
# From the project root
cd C:\Users\bejug\Projects\payroll_tool
docker-compose up -d postgres
docker-compose up backend
```

### 2. Local Development Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export DATABASE_URL=postgresql://payroll_user:payroll_pass@localhost:5432/payroll_db

# Run migrations
alembic upgrade head

# Start the server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Database Migrations

### Create a new migration
```bash
alembic revision --autogenerate -m "description"
```

### Apply migrations
```bash
alembic upgrade head
```

### Rollback migration
```bash
alembic downgrade -1
```

## API Documentation

Once the server is running, access the interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### College Management
- `GET /api/v1/colleges` - List colleges
- `POST /api/v1/colleges` - Create college
- `POST /api/v1/colleges/bulk` - Bulk create colleges
- `GET /api/v1/colleges/{id}` - Get college
- `PUT /api/v1/colleges/{id}` - Update college
- `DELETE /api/v1/colleges/{id}` - Delete college

### Employee Management
- `GET /api/v1/employees` - List employees (with filters)
- `POST /api/v1/employees` - Create employee
- `POST /api/v1/employees/bulk` - Bulk create employees
- `GET /api/v1/employees/{id}` - Get employee
- `PUT /api/v1/employees/{id}` - Update employee
- `DELETE /api/v1/employees/{id}` - Soft delete employee

### Attendance Management
- `GET /api/v1/attendance/uploads` - List attendance uploads
- `POST /api/v1/attendance/upload` - Upload attendance Excel
- `GET /api/v1/attendance/records` - List attendance records

### Payroll Processing
- `GET /api/v1/payroll/cycles` - List payroll cycles
- `POST /api/v1/payroll/calculate` - Calculate payroll
- `GET /api/v1/payroll/entries` - List payroll entries
- `GET /api/v1/payroll/summary` - Get payroll summary

### Payslip Management
- `GET /api/v1/payslips` - List payslips
- `GET /api/v1/payslips/{id}` - Get payslip
- `GET /api/v1/payslips/{id}/download` - Download payslip PDF
- `POST /api/v1/payslips/generate/{cycle_id}` - Generate payslips

### Reports
- `GET /api/v1/reports` - List reports
- `POST /api/v1/reports/generate` - Generate report
- `GET /api/v1/reports/{id}/download` - Download report

## Database Schema

### Core Entities

1. **colleges** - College master data
2. **departments** - Department within colleges
3. **designations** - Job designations
4. **salary_components** - Salary component definitions (earnings/deductions)
5. **employees** - Employee master data
6. **employee_salary_structures** - Employee salary breakup
7. **leave_policies** - Leave policies per college
8. **employee_leave_balances** - Employee leave balances per year
9. **attendance_uploads** - Uploaded attendance file metadata
10. **attendance_records** - Daily attendance records
11. **holidays** - Holiday calendar per college
12. **payroll_cycles** - Monthly payroll cycles
13. **payroll_entries** - Calculated payroll per employee
14. **payroll_entry_components** - Component-wise payroll breakdown
15. **payslips** - Generated payslip metadata
16. **reports** - Generated report metadata

## Environment Variables

```env
# Application
APP_NAME=Aurora Group Payroll Management
DEBUG=True

# Database
DATABASE_URL=postgresql://payroll_user:payroll_pass@localhost:5432/payroll_db

# Storage
STORAGE_PATH=storage
UPLOAD_PATH=storage/uploads
PAYSLIP_PATH=storage/payslips
REPORT_PATH=storage/reports

# Pagination
DEFAULT_PAGE_SIZE=50
MAX_PAGE_SIZE=200

# Leave Configuration
DEFAULT_PAID_LEAVES_PER_YEAR=12
DEFAULT_MAX_CARRY_FORWARD=5
```

## Development

### Code Quality
- Follow PEP 8 style guide
- Use type hints
- Write docstrings for functions
- Keep functions small and focused

### Testing
```bash
# Run tests (when implemented)
pytest
```

## Deployment

### Production Checklist
- [ ] Set DEBUG=False
- [ ] Configure proper DATABASE_URL
- [ ] Set strong SECRET_KEY
- [ ] Configure CORS origins
- [ ] Set up SSL/TLS
- [ ] Configure backup strategy
- [ ] Set up monitoring
- [ ] Configure logging

## Support

For issues and questions, contact the development team.

## License

Proprietary - Aurora Group
