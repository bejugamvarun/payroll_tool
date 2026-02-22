from typing import Optional
from datetime import datetime
from pathlib import Path
from sqlalchemy.orm import Session
from app.models.reports import Report
from app.utils.report_generator import generate_salary_statement, generate_consolidated_report
from app.config import settings


def generate_report(
    college_id: Optional[int],
    year: int,
    month: int,
    report_type: str,
    db: Session
) -> Report:
    """
    Generate a report and save it to the database.

    Args:
        college_id: College ID (None for consolidated reports)
        year: Year
        month: Month
        report_type: Type of report (salary_statement, consolidated)
        db: Database session

    Returns:
        Report object
    """
    # Create reports directory
    reports_dir = Path(settings.REPORT_PATH)
    reports_dir.mkdir(parents=True, exist_ok=True)

    # Generate filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    if report_type == "salary_statement" and college_id:
        filename = f"salary_statement_college{college_id}_{year}_{month:02d}_{timestamp}.xlsx"
        output_path = reports_dir / filename

        # Generate report
        generate_salary_statement(college_id, year, month, db, str(output_path))

        report_name = f"Salary Statement - College {college_id} - {month:02d}/{year}"

    elif report_type == "consolidated":
        filename = f"consolidated_report_{year}_{month:02d}_{timestamp}.xlsx"
        output_path = reports_dir / filename

        # Generate consolidated report
        generate_consolidated_report(year, month, db, str(output_path))

        report_name = f"Consolidated Report - {month:02d}/{year}"

    else:
        raise ValueError(f"Invalid report type: {report_type}")

    # Create Report record
    report = Report(
        report_type=report_type,
        file_path=str(output_path),
        college_id=college_id,
        year=year,
        month=month
    )

    db.add(report)
    db.commit()
    db.refresh(report)

    return report
