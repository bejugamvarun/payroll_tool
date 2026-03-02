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
from app.models import College, Department, Designation, SalaryComponent, ComponentType, AppliesTo

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
    for name in ['Professor', 'Associate Professor', 'Assistant Professor', 'Senior Lecturer', 'Lecturer', 'Lab Instructor', 'Principal', 'Vice Principal', 'Dean', 'HOD (Head of Department)', 'Registrar', 'Controller of Examinations', 'Librarian', 'Assistant Librarian', 'Administrative Officer', 'Senior Assistant', 'Junior Assistant', 'Office Attendant', 'Lab Technician', 'Peon', 'IT Manager', 'System Administrator', 'Network Engineer', 'HR Manager', 'Accountant', 'Cashier', 'Floor Incharge', 'Security', 'Housekeeping Staff', 'Driver']:
        db.add(Designation(name=name, college_id=None))
    db.commit()

    # ---------------------------------------------------------------------------
    # Salary Components - sourced from real Excel payroll sheets
    # Each entry: (name, component_type, applies_to, is_percentage, percentage_value, percentage_of, description)
    # ---------------------------------------------------------------------------
    EARNING = ComponentType.EARNING
    DEDUCTION = ComponentType.DEDUCTION
    ALL = AppliesTo.ALL
    TEACHING = AppliesTo.TEACHING
    NON_TEACHING = AppliesTo.NON_TEACHING
    SUB_STAFF = AppliesTo.SUB_STAFF

    components = [
        # ---- Earnings common to all staff types ----
        ('Basic Salary',                        EARNING,   ALL,         False, None,  None,    'Basic pay component'),
        ('Dearness Allowance (DA)',              EARNING,   ALL,         False, None,  None,    'Cost of living adjustment'),
        ('House Rent Allowance (HRA)',           EARNING,   ALL,         False, None,  None,    'Housing allowance'),

        # ---- Earnings for Teaching Staff ----
        ('City Compensatory Allowance (CCA)',   EARNING,   TEACHING,    False, None,  None,    'Fixed city compensatory allowance for teaching staff (Rs.250)'),
        ('I/C / HOD Allowance',                 EARNING,   TEACHING,    False, None,  None,    'In-charge or Head of Department allowance'),
        ('Research / Additional Allowance',     EARNING,   TEACHING,    False, None,  None,    'Research or additional responsibility allowance'),
        ('Conv / Car / Fuel Allowance',         EARNING,   TEACHING,    False, None,  None,    'Conveyance, car or fuel allowance for teaching staff'),
        ('Other / Administrative Allowance',    EARNING,   TEACHING,    False, None,  None,    'Other or administrative coordinator allowance for teaching staff'),
        ('Driver Salary',                       EARNING,   TEACHING,    False, None,  None,    'Driver salary paid through the employee payslip'),
        ('Retention Allowance',                 EARNING,   TEACHING,    False, None,  None,    'Retention allowance for teaching staff'),

        # ---- Earnings for Non-Teaching Staff ----
        ('City Compensatory Allowance (CCA)',   EARNING,   NON_TEACHING, False, None, None,    'Fixed city compensatory allowance for non-teaching staff (Rs.150-200)'),
        ('Conveyance Allowance',                EARNING,   NON_TEACHING, False, None, None,    'Conveyance allowance for non-teaching staff'),
        ('Children Education Allowance (CEA)',  EARNING,   NON_TEACHING, False, None, None,    'Children education allowance'),
        ('Grooming Allowance',                  EARNING,   NON_TEACHING, False, None, None,    'Grooming allowance for non-teaching staff'),
        ('Other Allowance',                     EARNING,   NON_TEACHING, False, None, None,    'Other allowance for non-teaching staff'),

        # ---- Earnings for Sub Staff ----
        ('Conveyance Allowance',                EARNING,   SUB_STAFF,   False, None,  None,    'Conveyance allowance for sub staff'),
        ('Other Allowance',                     EARNING,   SUB_STAFF,   False, None,  None,    'Other allowance for sub staff'),
        ('Floor Incharge Allowance',            EARNING,   SUB_STAFF,   False, None,  None,    'Additional allowance for floor incharge role'),

        # ---- Deductions common to all staff types ----
        ('Provident Fund (PF 12%)',             DEDUCTION, ALL,         True,  12.00, 'BASIC', 'Employee provident fund contribution at 12% of basic salary'),
        ('ESI (0.75%)',                         DEDUCTION, ALL,         True,  0.75,  'GROSS', 'Employee State Insurance at 0.75% of gross (applicable when gross is below ESI ceiling)'),
        ('Professional Tax (PT)',               DEDUCTION, ALL,         False, None,  None,    'State professional tax (fixed slab based on gross salary)'),
        ('Telephone Expenses',                  DEDUCTION, ALL,         False, None,  None,    'Telephone expense recovery'),
        ('Loss of Pay (LOP)',                   DEDUCTION, ALL,         False, None,  None,    'Deduction for loss of pay days (calculated from LOP days and per-day salary)'),

        # ---- Deductions for Teaching Staff only ----
        ('Income Tax (TDS)',                    DEDUCTION, TEACHING,    False, None,  None,    'Tax deducted at source for teaching staff'),
        ('Driver Salary Recovery',              DEDUCTION, TEACHING,    False, None,  None,    'Recovery of driver salary paid through payslip'),

        # ---- Deductions for Non-Teaching Staff only ----
        ('Mobile Expenses',                     DEDUCTION, NON_TEACHING, False, None, None,    'Mobile expense recovery for non-teaching staff'),
        ('Salary Advance Recovery',             DEDUCTION, NON_TEACHING, False, None, None,    'Recovery of salary advance for non-teaching staff'),
    ]

    for (name, ctype, applies, is_pct, pct_val, pct_of, desc) in components:
        db.add(SalaryComponent(
            name=name,
            component_type=ctype,
            applies_to=applies,
            is_default=True,
            is_percentage=is_pct,
            percentage_value=pct_val,
            percentage_of=pct_of,
            description=desc,
        ))
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
