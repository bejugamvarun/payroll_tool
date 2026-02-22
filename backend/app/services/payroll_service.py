from typing import Optional
from decimal import Decimal
from datetime import datetime, date
from sqlalchemy.orm import Session
from sqlalchemy import and_
from calendar import monthrange
from app.models.payroll_cycles import PayrollCycle, PayrollCycleStatus
from app.models.payroll_entries import PayrollEntry
from app.models.payroll_entry_components import PayrollEntryComponent
from app.models.employees import Employee
from app.models.employee_leave_balances import EmployeeLeaveBalance
from app.models.employee_salary_structures import EmployeeSalaryStructure
from app.models.attendance_records import AttendanceRecord, AttendanceStatus
from app.models.holidays import Holiday
from app.models.salary_components import SalaryComponent, ComponentType
from app.utils.date_utils import get_working_days
from app.config import settings


def calculate_payroll(college_id: int, year: int, month: int, db: Session) -> PayrollCycle:
    """
    Calculate payroll for a specific college, year, and month.

    This is the core payroll calculation engine that:
    1. Creates or updates a payroll cycle
    2. Calculates working days
    3. Processes each employee's attendance
    4. Applies leave waterfall logic
    5. Calculates salary components
    6. Creates payroll entries

    Args:
        college_id: College ID
        year: Year
        month: Month
        db: Database session

    Returns:
        PayrollCycle object
    """
    # Step 1: Get or create PayrollCycle
    cycle = db.query(PayrollCycle).filter(
        PayrollCycle.college_id == college_id,
        PayrollCycle.year == year,
        PayrollCycle.month == month
    ).first()

    if cycle:
        if cycle.status == PayrollCycleStatus.LOCKED:
            raise ValueError(f"Payroll cycle for {college_id}-{year}-{month} is locked")

        # Delete existing entries if recalculating
        db.query(PayrollEntry).filter(PayrollEntry.payroll_cycle_id == cycle.id).delete()
        db.commit()
    else:
        cycle = PayrollCycle(
            college_id=college_id,
            year=year,
            month=month,
            total_working_days=0,
            status=PayrollCycleStatus.DRAFT
        )
        db.add(cycle)
        db.flush()

    # Update status to PROCESSING
    cycle.status = PayrollCycleStatus.PROCESSING
    db.commit()

    try:
        # Step 2: Get holidays for this college and month
        start_date = date(year, month, 1)
        _, last_day = monthrange(year, month)
        end_date = date(year, month, last_day)

        holidays = db.query(Holiday).filter(
            Holiday.college_id == college_id,
            Holiday.date >= start_date,
            Holiday.date <= end_date
        ).all()

        holiday_dates = [h.date for h in holidays]

        # Step 3: Calculate total working days
        total_working_days = get_working_days(
            year,
            month,
            holiday_dates,
            settings.WEEKEND_DAYS
        )

        cycle.total_working_days = total_working_days
        db.commit()

        # Step 4: Get all active employees for this college
        employees = db.query(Employee).filter(
            Employee.college_id == college_id,
            Employee.is_active == True
        ).all()

        # Step 5: Process each employee
        for employee in employees:
            # Get attendance records for the month
            attendance_records = db.query(AttendanceRecord).filter(
                AttendanceRecord.employee_id == employee.id,
                AttendanceRecord.date >= start_date,
                AttendanceRecord.date <= end_date
            ).all()

            # Calculate days present and weekend work
            days_present = Decimal(0)
            weekend_work_count = Decimal(0)

            for record in attendance_records:
                if record.status == AttendanceStatus.PRESENT:
                    days_present += Decimal(1)
                elif record.status == AttendanceStatus.HALF_DAY:
                    days_present += Decimal("0.5")
                elif record.status == AttendanceStatus.WEEKEND_WORK:
                    weekend_work_count += Decimal(1)
                    days_present += Decimal(1)

            # Calculate days absent (only counting working days)
            days_absent = Decimal(total_working_days) - days_present

            # Get or create employee leave balance for this year
            leave_balance = db.query(EmployeeLeaveBalance).filter(
                EmployeeLeaveBalance.employee_id == employee.id,
                EmployeeLeaveBalance.year == year
            ).first()

            if not leave_balance:
                # Create leave balance if it doesn't exist
                leave_balance = EmployeeLeaveBalance(
                    employee_id=employee.id,
                    year=year,
                    paid_leaves_total=Decimal(settings.DEFAULT_PAID_LEAVES_PER_YEAR),
                    paid_leaves_used=Decimal(0),
                    comp_leaves_earned=Decimal(0),
                    comp_leaves_used=Decimal(0),
                    carry_forward_leaves=Decimal(0)
                )
                db.add(leave_balance)
                db.flush()

            # Credit comp leaves for weekend work
            leave_balance.comp_leaves_earned += weekend_work_count

            # Apply leave waterfall for absences
            remaining_absences = days_absent
            paid_leaves_used = Decimal(0)
            comp_leaves_used = Decimal(0)
            unpaid_leaves = Decimal(0)

            # Calculate available leaves
            paid_leaves_available = (
                leave_balance.paid_leaves_total +
                leave_balance.carry_forward_leaves -
                leave_balance.paid_leaves_used
            )
            comp_leaves_available = (
                leave_balance.comp_leaves_earned -
                leave_balance.comp_leaves_used
            )

            # First, use paid leaves
            if remaining_absences > 0 and paid_leaves_available > 0:
                used = min(remaining_absences, paid_leaves_available)
                paid_leaves_used = used
                remaining_absences -= used

            # Then, use comp leaves
            if remaining_absences > 0 and comp_leaves_available > 0:
                used = min(remaining_absences, comp_leaves_available)
                comp_leaves_used = used
                remaining_absences -= used

            # Remaining are unpaid leaves
            unpaid_leaves = remaining_absences

            # Calculate per-day salary
            per_day_salary = employee.monthly_gross / Decimal(total_working_days)

            # Calculate loss of pay
            loss_of_pay = unpaid_leaves * per_day_salary

            # Get employee's salary structure (active components)
            salary_structures = db.query(EmployeeSalaryStructure).filter(
                EmployeeSalaryStructure.employee_id == employee.id,
                EmployeeSalaryStructure.effective_from <= end_date,
                and_(
                    EmployeeSalaryStructure.effective_to.is_(None) |
                    (EmployeeSalaryStructure.effective_to >= start_date)
                )
            ).all()

            # Calculate earnings and deductions
            gross_earnings = Decimal(0)
            total_deductions = Decimal(0)
            component_amounts = []

            for structure in salary_structures:
                component = structure.salary_component
                amount = structure.amount

                component_amounts.append({
                    "component_id": component.id,
                    "component_type": component.component_type,
                    "amount": amount
                })

                if component.component_type == ComponentType.EARNING:
                    gross_earnings += amount
                else:
                    total_deductions += amount

            # Add loss of pay to deductions
            total_deductions += loss_of_pay

            # Calculate net pay
            net_pay = gross_earnings - total_deductions

            # Create PayrollEntry
            payroll_entry = PayrollEntry(
                payroll_cycle_id=cycle.id,
                employee_id=employee.id,
                days_present=days_present,
                days_absent=days_absent,
                paid_leaves_used=paid_leaves_used,
                comp_leaves_used=comp_leaves_used,
                unpaid_leaves=unpaid_leaves,
                loss_of_pay=loss_of_pay,
                gross_earnings=gross_earnings,
                total_deductions=total_deductions,
                net_pay=net_pay
            )

            db.add(payroll_entry)
            db.flush()

            # Create PayrollEntryComponent records
            for comp_data in component_amounts:
                entry_component = PayrollEntryComponent(
                    payroll_entry_id=payroll_entry.id,
                    salary_component_id=comp_data["component_id"],
                    component_type=comp_data["component_type"],
                    amount=comp_data["amount"]
                )
                db.add(entry_component)

            # Update leave balance
            leave_balance.paid_leaves_used += paid_leaves_used
            leave_balance.comp_leaves_used += comp_leaves_used

        # Step 6: Mark cycle as completed
        cycle.status = PayrollCycleStatus.COMPLETED
        db.commit()

        return cycle

    except Exception as e:
        # Rollback on error
        db.rollback()
        cycle.status = PayrollCycleStatus.DRAFT
        db.commit()
        raise e


def lock_payroll_cycle(cycle_id: int, db: Session) -> PayrollCycle:
    """
    Lock a payroll cycle to prevent further modifications.

    Args:
        cycle_id: PayrollCycle ID
        db: Database session

    Returns:
        PayrollCycle object
    """
    cycle = db.query(PayrollCycle).filter(PayrollCycle.id == cycle_id).first()

    if not cycle:
        raise ValueError(f"Payroll cycle with ID {cycle_id} not found")

    if cycle.status == PayrollCycleStatus.LOCKED:
        raise ValueError(f"Payroll cycle {cycle_id} is already locked")

    if cycle.status != PayrollCycleStatus.COMPLETED:
        raise ValueError(f"Cannot lock payroll cycle {cycle_id} - it must be in COMPLETED status")

    cycle.status = PayrollCycleStatus.LOCKED
    cycle.locked_at = datetime.utcnow()
    db.commit()

    return cycle
