"""
Database seeding script to populate initial data for Aurora Group.
This creates sample colleges, departments, designations, and salary components.

Usage:
    python seed_data.py
"""

from app.database import SessionLocal
from app.models import (
    College, Department, Designation, SalaryComponent, ComponentType
)
from datetime import datetime


def seed_colleges(db):
    """Seed sample colleges"""
    print("Seeding colleges...")
    colleges = [
        College(serial_number=1, college_code="AUR001", name="Aurora Engineering College", address="Bhongir, Telangana"),
        College(serial_number=2, college_code="AUR002", name="Aurora College of Pharmacy", address="Hyderabad, Telangana"),
        College(serial_number=3, college_code="AUR003", name="Aurora Business School", address="Hyderabad, Telangana"),
        College(serial_number=4, college_code="AUR004", name="Aurora Degree College", address="Ghatkesar, Telangana"),
        College(serial_number=5, college_code="AUR005", name="Aurora PG College", address="Ramanthapur, Telangana"),
    ]

    for college in colleges:
        db.add(college)

    db.commit()
    print(f"✓ Created {len(colleges)} colleges")
    return colleges


def seed_departments(db, colleges):
    """Seed departments for each college"""
    print("Seeding departments...")

    engineering_depts = [
        "Computer Science & Engineering",
        "Electronics & Communication Engineering",
        "Mechanical Engineering",
        "Civil Engineering",
        "Electrical & Electronics Engineering",
        "Information Technology"
    ]

    pharmacy_depts = [
        "Pharmaceutics",
        "Pharmaceutical Chemistry",
        "Pharmacology",
        "Pharmacognosy"
    ]

    business_depts = [
        "Management Studies",
        "Commerce",
        "Finance & Accounting"
    ]

    general_depts = [
        "English",
        "Mathematics",
        "Physics",
        "Chemistry",
        "Administration"
    ]

    dept_count = 0

    for college in colleges:
        if "Engineering" in college.name:
            depts = engineering_depts
        elif "Pharmacy" in college.name:
            depts = pharmacy_depts
        elif "Business" in college.name:
            depts = business_depts
        else:
            depts = general_depts

        for dept_name in depts:
            dept = Department(college_id=college.id, name=dept_name)
            db.add(dept)
            dept_count += 1

    db.commit()
    print(f"✓ Created {dept_count} departments")


def seed_designations(db):
    """Seed common designations"""
    print("Seeding designations...")

    designations = [
        # Faculty
        "Professor",
        "Associate Professor",
        "Assistant Professor",
        "Senior Lecturer",
        "Lecturer",
        "Lab Instructor",
        # Administrative Staff
        "Principal",
        "Vice Principal",
        "Dean",
        "HOD (Head of Department)",
        "Registrar",
        "Controller of Examinations",
        "Librarian",
        "Assistant Librarian",
        # Support Staff
        "Administrative Officer",
        "Senior Assistant",
        "Junior Assistant",
        "Office Attendant",
        "Lab Technician",
        "Peon",
        # IT & Technical
        "IT Manager",
        "System Administrator",
        "Network Engineer",
        # HR & Finance
        "HR Manager",
        "Accountant",
        "Cashier"
    ]

    for designation_name in designations:
        designation = Designation(name=designation_name, college_id=None)
        db.add(designation)

    db.commit()
    print(f"✓ Created {len(designations)} designations")


def seed_salary_components(db):
    """Seed standard salary components"""
    print("Seeding salary components...")

    earnings = [
        ("Basic Salary", "Basic pay component"),
        ("House Rent Allowance (HRA)", "Housing allowance"),
        ("Dearness Allowance (DA)", "Cost of living adjustment"),
        ("Special Allowance", "Special pay component"),
        ("Medical Allowance", "Medical expenses coverage"),
        ("Transport Allowance", "Travel expenses"),
        ("Education Allowance", "Children education support"),
        ("Performance Bonus", "Performance-based bonus"),
    ]

    deductions = [
        ("Provident Fund (PF)", "Employee provident fund"),
        ("Professional Tax", "State professional tax"),
        ("Income Tax (TDS)", "Tax deducted at source"),
        ("ESI (Employee State Insurance)", "Health insurance contribution"),
        ("Loss of Pay (LOP)", "Deduction for unpaid leaves"),
    ]

    comp_count = 0

    for name, description in earnings:
        component = SalaryComponent(
            name=name,
            component_type=ComponentType.EARNING,
            is_default=True,
            description=description
        )
        db.add(component)
        comp_count += 1

    for name, description in deductions:
        component = SalaryComponent(
            name=name,
            component_type=ComponentType.DEDUCTION,
            is_default=True,
            description=description
        )
        db.add(component)
        comp_count += 1

    db.commit()
    print(f"✓ Created {comp_count} salary components")


def seed_all():
    """Seed all initial data"""
    print("=" * 60)
    print("Aurora Group Payroll Management System - Data Seeding")
    print("=" * 60)
    print()

    db = SessionLocal()

    try:
        # Check if data already exists
        existing_colleges = db.query(College).count()
        if existing_colleges > 0:
            print(f"⚠ Database already contains {existing_colleges} colleges.")
            response = input("Do you want to continue? This will add more data. (y/N): ")
            if response.lower() != 'y':
                print("Seeding cancelled.")
                return

        # Seed data
        colleges = seed_colleges(db)
        seed_departments(db, colleges)
        seed_designations(db)
        seed_salary_components(db)

        print()
        print("=" * 60)
        print("✓ Database seeding completed successfully!")
        print("=" * 60)
        print()
        print("Summary:")
        print(f"  - Colleges: {db.query(College).count()}")
        print(f"  - Departments: {db.query(Department).count()}")
        print(f"  - Designations: {db.query(Designation).count()}")
        print(f"  - Salary Components: {db.query(SalaryComponent).count()}")
        print()
        print("You can now:")
        print("  1. Access the API at http://localhost:8000/docs")
        print("  2. Run test_api.py to verify the setup")
        print("  3. Start adding employees and processing payroll")

    except Exception as e:
        print(f"✗ Error during seeding: {e}")
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    seed_all()
