#!/bin/bash
set -e

echo "============================================"
echo "  Aurora Group Payroll - Starting Up"
echo "============================================"

# Wait for postgres using Python/psycopg2 (no postgresql-client needed)
echo "Waiting for PostgreSQL..."
python -c "
import time, psycopg2, os
dsn = os.environ['DATABASE_URL']
while True:
    try:
        conn = psycopg2.connect(dsn)
        conn.close()
        break
    except psycopg2.OperationalError:
        print('  PostgreSQL not ready yet, retrying in 2s...')
        time.sleep(2)
"
echo "PostgreSQL is ready."

# Run Alembic migrations
echo ""
echo "Running database migrations..."
alembic upgrade head
echo "Migrations applied successfully."

# Seed data if the database is empty
COLLEGE_COUNT=$(python -c "
import psycopg2, os
conn = psycopg2.connect(os.environ['DATABASE_URL'])
cur = conn.cursor()
cur.execute('SELECT count(*) FROM colleges')
print(cur.fetchone()[0])
conn.close()
" 2>/dev/null || echo "0")

if [ "$COLLEGE_COUNT" = "0" ]; then
  echo ""
  echo "Empty database detected - seeding initial data..."
  python -c "
from app.database import SessionLocal
from app.models import College, Department, Designation, SalaryComponent, ComponentType

db = SessionLocal()
try:
    # Colleges
    colleges = [
        College(serial_number=1, college_code='AUR001', name='Aurora Engineering College', address='Bhongir, Telangana'),
        College(serial_number=2, college_code='AUR002', name='Aurora College of Pharmacy', address='Hyderabad, Telangana'),
        College(serial_number=3, college_code='AUR003', name='Aurora Business School', address='Hyderabad, Telangana'),
        College(serial_number=4, college_code='AUR004', name='Aurora Degree College', address='Ghatkesar, Telangana'),
        College(serial_number=5, college_code='AUR005', name='Aurora PG College', address='Ramanthapur, Telangana'),
    ]
    for c in colleges:
        db.add(c)
    db.commit()

    # Departments
    dept_map = {
        'Engineering': ['Computer Science & Engineering', 'Electronics & Communication Engineering', 'Mechanical Engineering', 'Civil Engineering', 'Electrical & Electronics Engineering', 'Information Technology'],
        'Pharmacy': ['Pharmaceutics', 'Pharmaceutical Chemistry', 'Pharmacology', 'Pharmacognosy'],
        'Business': ['Management Studies', 'Commerce', 'Finance & Accounting'],
    }
    general = ['English', 'Mathematics', 'Physics', 'Chemistry', 'Administration']
    for college in colleges:
        matched = False
        for keyword, depts in dept_map.items():
            if keyword in college.name:
                for d in depts:
                    db.add(Department(college_id=college.id, name=d))
                matched = True
                break
        if not matched:
            for d in general:
                db.add(Department(college_id=college.id, name=d))
    db.commit()

    # Designations
    for name in ['Professor', 'Associate Professor', 'Assistant Professor', 'Senior Lecturer', 'Lecturer', 'Lab Instructor', 'Principal', 'Vice Principal', 'Dean', 'HOD (Head of Department)', 'Registrar', 'Controller of Examinations', 'Librarian', 'Assistant Librarian', 'Administrative Officer', 'Senior Assistant', 'Junior Assistant', 'Office Attendant', 'Lab Technician', 'Peon', 'IT Manager', 'System Administrator', 'Network Engineer', 'HR Manager', 'Accountant', 'Cashier']:
        db.add(Designation(name=name, college_id=None))
    db.commit()

    # Salary Components
    for name, desc in [('Basic Salary', 'Basic pay component'), ('House Rent Allowance (HRA)', 'Housing allowance'), ('Dearness Allowance (DA)', 'Cost of living adjustment'), ('Special Allowance', 'Special pay component'), ('Medical Allowance', 'Medical expenses coverage'), ('Transport Allowance', 'Travel expenses'), ('Education Allowance', 'Children education support'), ('Performance Bonus', 'Performance-based bonus')]:
        db.add(SalaryComponent(name=name, component_type=ComponentType.EARNING, is_default=True, description=desc))
    for name, desc in [('Provident Fund (PF)', 'Employee provident fund'), ('Professional Tax', 'State professional tax'), ('Income Tax (TDS)', 'Tax deducted at source'), ('ESI (Employee State Insurance)', 'Health insurance contribution'), ('Loss of Pay (LOP)', 'Deduction for unpaid leaves')]:
        db.add(SalaryComponent(name=name, component_type=ComponentType.DEDUCTION, is_default=True, description=desc))
    db.commit()

    print('Seed data inserted successfully.')
finally:
    db.close()
"
  echo "Database seeded."
else
  echo "Database already has data ($COLLEGE_COUNT colleges) - skipping seed."
fi

echo ""
echo "============================================"
echo "  Starting Uvicorn server..."
echo "============================================"

exec uvicorn app.main:app --host 0.0.0.0 --port 8000
