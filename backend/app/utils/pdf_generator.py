from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from datetime import datetime
from decimal import Decimal
from app.models.payroll_entries import PayrollEntry
from app.models.salary_components import ComponentType


def generate_payslip_pdf(payroll_entry: PayrollEntry, output_path: str) -> str:
    """
    Generate a payslip PDF for a given payroll entry.

    Args:
        payroll_entry: PayrollEntry object with all relationships loaded
        output_path: Path where the PDF should be saved

    Returns:
        Path to the generated PDF file
    """
    doc = SimpleDocTemplate(output_path, pagesize=A4)
    story = []
    styles = getSampleStyleSheet()

    # Custom styles
    title_style = styles['Heading1']
    title_style.alignment = TA_CENTER

    heading_style = styles['Heading2']
    heading_style.fontSize = 12

    normal_style = styles['Normal']
    normal_style.fontSize = 10

    # Company Header
    story.append(Paragraph("AURORA GROUP", title_style))
    story.append(Spacer(1, 0.2 * inch))

    # Payslip Title
    payslip_title = f"PAYSLIP - {payroll_entry.payroll_cycle.month:02d}/{payroll_entry.payroll_cycle.year}"
    story.append(Paragraph(payslip_title, heading_style))
    story.append(Spacer(1, 0.2 * inch))

    # Employee Details
    employee = payroll_entry.employee
    college = employee.college
    department = employee.department
    designation = employee.designation

    employee_data = [
        ["Employee Code:", employee.employee_code, "College:", college.name],
        ["Name:", f"{employee.first_name} {employee.last_name}", "Department:", department.name],
        ["Designation:", designation.name, "PAN:", employee.pan_number or "N/A"],
        ["Bank:", employee.bank_name or "N/A", "Account No:", employee.bank_account_number or "N/A"],
        ["IFSC Code:", employee.ifsc_code or "N/A", "", ""],
    ]

    employee_table = Table(employee_data, colWidths=[1.5 * inch, 2.5 * inch, 1.5 * inch, 2.5 * inch])
    employee_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (2, 0), (2, -1), 'Helvetica-Bold'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))

    story.append(employee_table)
    story.append(Spacer(1, 0.3 * inch))

    # Salary Components - Earnings and Deductions side by side
    earnings = []
    deductions = []

    for component in payroll_entry.components:
        if component.component_type == ComponentType.EARNING:
            earnings.append([
                component.salary_component.name,
                f"₹ {float(component.amount):,.2f}"
            ])
        else:
            deductions.append([
                component.salary_component.name,
                f"₹ {float(component.amount):,.2f}"
            ])

    # Add Loss of Pay to deductions if present
    if payroll_entry.loss_of_pay > 0:
        deductions.append([
            "Loss of Pay",
            f"₹ {float(payroll_entry.loss_of_pay):,.2f}"
        ])

    # Ensure equal rows
    max_rows = max(len(earnings), len(deductions))
    while len(earnings) < max_rows:
        earnings.append(["", ""])
    while len(deductions) < max_rows:
        deductions.append(["", ""])

    # Create component table
    component_header = [["EARNINGS", "AMOUNT", "DEDUCTIONS", "AMOUNT"]]
    component_data = component_header + [
        [e[0], e[1], d[0], d[1]]
        for e, d in zip(earnings, deductions)
    ]

    # Add totals
    component_data.append([
        "GROSS EARNINGS",
        f"₹ {float(payroll_entry.gross_earnings):,.2f}",
        "TOTAL DEDUCTIONS",
        f"₹ {float(payroll_entry.total_deductions):,.2f}"
    ])

    component_table = Table(component_data, colWidths=[2.5 * inch, 1.5 * inch, 2.5 * inch, 1.5 * inch])
    component_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
        ('ALIGN', (3, 0), (3, -1), 'RIGHT'),
        ('FONTNAME', (0, 1), (-1, -2), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -2), 9),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, -1), (-1, -1), 10),
        ('BACKGROUND', (0, -1), (-1, -1), colors.lightgrey),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))

    story.append(component_table)
    story.append(Spacer(1, 0.2 * inch))

    # Net Pay
    net_pay_data = [[
        "NET PAY",
        f"₹ {float(payroll_entry.net_pay):,.2f}"
    ]]

    net_pay_table = Table(net_pay_data, colWidths=[6.5 * inch, 1.5 * inch])
    net_pay_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('BACKGROUND', (0, 0), (-1, -1), colors.green),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.whitesmoke),
        ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))

    story.append(net_pay_table)
    story.append(Spacer(1, 0.3 * inch))

    # Attendance Summary
    cycle = payroll_entry.payroll_cycle
    attendance_data = [
        ["Working Days", "Present Days", "Paid Leaves", "Comp Leaves", "Unpaid Leaves"],
        [
            str(cycle.total_working_days),
            str(float(payroll_entry.days_present)),
            str(float(payroll_entry.paid_leaves_used)),
            str(float(payroll_entry.comp_leaves_used)),
            str(float(payroll_entry.unpaid_leaves))
        ]
    ]

    attendance_table = Table(attendance_data, colWidths=[1.6 * inch] * 5)
    attendance_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))

    story.append(attendance_table)
    story.append(Spacer(1, 0.5 * inch))

    # Footer
    footer_text = f"Generated on: {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}"
    story.append(Paragraph(footer_text, normal_style))

    # Build PDF
    doc.build(story)

    return output_path
