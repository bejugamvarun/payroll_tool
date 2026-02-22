# Aurora Group Payroll Management System

A comprehensive payroll management system for Aurora Group, managing 20-25 colleges with approximately 200 employees per college (4,000-5,000 total employees).

## Overview

This system provides end-to-end payroll processing including:

- Multi-college and employee management
- Attendance tracking via Excel uploads
- Automated salary calculations with leave management
- Payslip PDF generation
- Comprehensive reporting
- Leave policy and balance tracking
- Holiday calendar management

## Technology Stack

### Backend
- **Framework**: FastAPI
- **Database**: PostgreSQL 15
- **ORM**: SQLAlchemy 2.0
- **Migrations**: Alembic
- **Excel Processing**: openpyxl, pandas
- **PDF Generation**: reportlab

### Frontend
- **Framework**: Vite + React (to be implemented)
- **Port**: 5173

### Infrastructure
- **Containerization**: Docker & Docker Compose
- **Database Port**: 5432
- **Backend Port**: 8000

## Quick Start

### Prerequisites
- Docker and Docker Compose
- Git

### Start the Application

```bash
# Clone the repository
cd C:\Users\bejug\Projects\payroll_tool

# Start all services
docker-compose up -d

# View logs
docker-compose logs -f backend
```

The services will be available at:
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs
- Frontend: http://localhost:5173 (when implemented)
- PostgreSQL: localhost:5432

### Initialize Database

```bash
# Run migrations
docker-compose exec backend alembic upgrade head
```

## Project Structure

```
payroll_tool/
├── backend/                 # FastAPI backend
│   ├── alembic/            # Database migrations
│   ├── app/
│   │   ├── models/         # SQLAlchemy models (14 entities)
│   │   ├── routers/        # API endpoints
│   │   ├── schemas/        # Pydantic schemas
│   │   ├── services/       # Business logic
│   │   ├── repositories/   # Data access layer
│   │   ├── utils/          # Utilities
│   │   ├── config.py       # Configuration
│   │   ├── database.py     # Database setup
│   │   └── main.py         # FastAPI app
│   ├── storage/            # File storage
│   │   ├── uploads/        # Attendance Excel files
│   │   ├── payslips/       # Generated PDFs
│   │   └── reports/        # Generated reports
│   ├── Dockerfile
│   ├── requirements.txt
│   └── README.md
├── frontend/               # Frontend (to be implemented)
├── docker-compose.yml      # Docker orchestration
└── README.md              # This file
```

## Database Schema

The system uses 16 core tables:

1. **colleges** - College master data
2. **departments** - Departments within colleges
3. **designations** - Job designations
4. **salary_components** - Salary component definitions
5. **employees** - Employee master data
6. **employee_salary_structures** - Employee salary breakup
7. **leave_policies** - Leave policies per college
8. **employee_leave_balances** - Employee leave balances
9. **attendance_uploads** - Attendance file metadata
10. **attendance_records** - Daily attendance records
11. **holidays** - Holiday calendar
12. **payroll_cycles** - Monthly payroll cycles
13. **payroll_entries** - Calculated payroll per employee
14. **payroll_entry_components** - Component-wise breakdown
15. **payslips** - Generated payslip metadata
16. **reports** - Generated report metadata

## Key Features

### 1. College & Employee Management
- Bulk create/update/delete operations
- Filter employees by college, department, status
- Soft delete support for employees

### 2. Attendance Management
- Upload Excel sheets from biometric devices
- Automatic parsing and validation
- Track present/absent/half-day/weekend work
- Support for multiple file formats

### 3. Leave Management
- Configurable leave policies per college
- Paid leave allocation and tracking
- Compensatory leave for weekend work
- Carry forward support
- Automatic leave balance updates

### 4. Payroll Processing
- Automated monthly salary calculations
- Working days calculation (excluding weekends and holidays)
- Leave-based deductions
- Loss of pay calculation
- Component-wise salary breakdown

### 5. Payslip Generation
- Professional PDF payslips
- Detailed earnings and deductions
- Leave balance summary
- Digital signature support

### 6. Reporting
- Salary register (college-wise or org-wide)
- Attendance summary reports
- Leave utilization reports
- College-wise payroll summary
- Year-to-date reports
- Excel/CSV export

## API Endpoints

### College Management
- `GET /api/v1/colleges` - List colleges
- `POST /api/v1/colleges` - Create college
- `POST /api/v1/colleges/bulk` - Bulk create

### Employee Management
- `GET /api/v1/employees` - List employees
- `POST /api/v1/employees` - Create employee
- `POST /api/v1/employees/bulk` - Bulk create

### Attendance
- `POST /api/v1/attendance/upload` - Upload Excel
- `GET /api/v1/attendance/records` - List records

### Payroll
- `POST /api/v1/payroll/calculate` - Calculate payroll
- `GET /api/v1/payroll/summary` - Get summary

### Payslips
- `GET /api/v1/payslips` - List payslips
- `GET /api/v1/payslips/{id}/download` - Download PDF

### Reports
- `POST /api/v1/reports/generate` - Generate report
- `GET /api/v1/reports/{id}/download` - Download report

For complete API documentation, visit http://localhost:8000/docs

## Development

### Backend Development

```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Run migrations
alembic upgrade head

# Start development server
uvicorn app.main:app --reload
```

### Database Migrations

```bash
# Create migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback
alembic downgrade -1
```

## Salary Calculation Logic

1. Calculate total working days (exclude weekends and holidays)
2. Parse attendance from uploaded Excel
3. Calculate leaves taken = working days - days present
4. Weekend work bonus: +1 compensatory leave per weekend day worked
5. Deduct from paid leaves first, then comp leaves, then unpaid
6. Per-day deduction = monthly_gross / working_days_in_month
7. Total deduction = unpaid_leave_days × per_day_salary
8. Net salary = monthly_gross - deductions

## Configuration

Key configuration in `backend/app/config.py`:

- Database connection
- Storage paths
- Pagination limits
- Leave policies
- CORS settings
- Weekend days configuration

## Support for Scale

Designed to handle:
- 4,000-5,000 employees
- 20-25 colleges
- Bulk operations with batch processing
- Connection pooling (pool_size: 20, max_overflow: 40)
- Async file processing
- Proper indexing on all query fields

## Security Considerations

- SQL injection protection via ORM
- Input validation with Pydantic
- CORS configuration
- Prepared for authentication/authorization
- Environment-based secrets

## Future Enhancements

- [ ] User authentication and RBAC
- [ ] Email notifications for payslips
- [ ] Automated monthly processing scheduler
- [ ] Advanced analytics dashboard
- [ ] Mobile app
- [ ] Integration with accounting systems
- [ ] Biometric device direct integration

## License

Proprietary - Aurora Group

## Contact

For support and inquiries, contact the Aurora Group IT team.
