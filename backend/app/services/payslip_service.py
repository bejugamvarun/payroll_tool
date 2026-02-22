import os
import zipfile
from typing import List
from pathlib import Path
from sqlalchemy.orm import Session
from app.models.payroll_cycles import PayrollCycle, PayrollCycleStatus
from app.models.payroll_entries import PayrollEntry
from app.models.payslips import Payslip
from app.utils.pdf_generator import generate_payslip_pdf
from app.config import settings


def generate_payslips_for_cycle(cycle_id: int, db: Session) -> List[Payslip]:
    """
    Generate payslip PDFs for all entries in a payroll cycle.

    Args:
        cycle_id: PayrollCycle ID
        db: Database session

    Returns:
        List of Payslip objects
    """
    # Get the payroll cycle
    cycle = db.query(PayrollCycle).filter(PayrollCycle.id == cycle_id).first()

    if not cycle:
        raise ValueError(f"Payroll cycle with ID {cycle_id} not found")

    if cycle.status not in [PayrollCycleStatus.COMPLETED, PayrollCycleStatus.LOCKED]:
        raise ValueError(f"Payroll cycle {cycle_id} must be COMPLETED or LOCKED to generate payslips")

    # Get all payroll entries for this cycle
    entries = db.query(PayrollEntry).filter(
        PayrollEntry.payroll_cycle_id == cycle_id
    ).all()

    if not entries:
        raise ValueError(f"No payroll entries found for cycle {cycle_id}")

    # Create directory structure: {PAYSLIP_PATH}/{college_code}/{year}/{month}/
    college = cycle.college
    payslip_dir = Path(settings.PAYSLIP_PATH) / college.college_code / str(cycle.year) / f"{cycle.month:02d}"
    payslip_dir.mkdir(parents=True, exist_ok=True)

    generated_payslips = []

    for entry in entries:
        # Check if payslip already exists
        existing_payslip = db.query(Payslip).filter(
            Payslip.payroll_entry_id == entry.id
        ).first()

        if existing_payslip:
            # Delete old payslip file if it exists
            if os.path.exists(existing_payslip.file_path):
                os.remove(existing_payslip.file_path)

            db.delete(existing_payslip)
            db.commit()

        # Generate PDF filename
        employee = entry.employee
        pdf_filename = f"{employee.employee_code}_payslip_{cycle.year}_{cycle.month:02d}.pdf"
        pdf_path = payslip_dir / pdf_filename

        # Generate the PDF
        generate_payslip_pdf(entry, str(pdf_path))

        # Create Payslip record
        payslip = Payslip(
            payroll_entry_id=entry.id,
            employee_id=employee.id,
            payroll_cycle_id=cycle.id,
            file_path=str(pdf_path)
        )

        db.add(payslip)
        generated_payslips.append(payslip)

    db.commit()

    return generated_payslips


def generate_bulk_zip(cycle_id: int, db: Session, output_path: str) -> str:
    """
    Generate a ZIP file containing all payslips for a payroll cycle.

    Args:
        cycle_id: PayrollCycle ID
        db: Database session
        output_path: Path where the ZIP file should be saved

    Returns:
        Path to the generated ZIP file
    """
    # Get all payslips for the cycle
    payslips = db.query(Payslip).filter(
        Payslip.payroll_cycle_id == cycle_id
    ).all()

    if not payslips:
        raise ValueError(f"No payslips found for cycle {cycle_id}")

    # Create ZIP file
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for payslip in payslips:
            if os.path.exists(payslip.file_path):
                # Add file to ZIP with employee code as the name
                employee = payslip.employee
                arcname = f"{employee.employee_code}_{employee.first_name}_{employee.last_name}.pdf"
                zipf.write(payslip.file_path, arcname=arcname)

    return output_path
