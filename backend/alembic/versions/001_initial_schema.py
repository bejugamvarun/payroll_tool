"""Initial schema creation

Revision ID: 001
Revises:
Create Date: 2026-02-23
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '001'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Enums
    componenttype = sa.Enum('EARNING', 'DEDUCTION', name='componenttype')
    uploadstatus = sa.Enum('PENDING', 'PROCESSING', 'COMPLETED', 'FAILED', name='uploadstatus')
    attendancestatus = sa.Enum('PRESENT', 'ABSENT', 'HALF_DAY', 'WEEKEND_WORK', 'HOLIDAY', 'LEAVE', name='attendancestatus')
    payrollcyclestatus = sa.Enum('DRAFT', 'PROCESSING', 'COMPLETED', 'LOCKED', name='payrollcyclestatus')

    componenttype.create(op.get_bind(), checkfirst=True)
    uploadstatus.create(op.get_bind(), checkfirst=True)
    attendancestatus.create(op.get_bind(), checkfirst=True)
    payrollcyclestatus.create(op.get_bind(), checkfirst=True)

    # 1. colleges
    op.create_table(
        'colleges',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('serial_number', sa.Integer(), nullable=False),
        sa.Column('college_code', sa.String(50), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('address', sa.String(500), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
    )
    op.create_index('ix_colleges_id', 'colleges', ['id'])
    op.create_index('ix_colleges_college_code', 'colleges', ['college_code'], unique=True)

    # 2. departments
    op.create_table(
        'departments',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('college_id', sa.Integer(), sa.ForeignKey('colleges.id'), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
    )
    op.create_index('ix_departments_id', 'departments', ['id'])
    op.create_index('ix_departments_college_id', 'departments', ['college_id'])

    # 3. designations
    op.create_table(
        'designations',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('college_id', sa.Integer(), sa.ForeignKey('colleges.id'), nullable=True),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
    )
    op.create_index('ix_designations_id', 'designations', ['id'])
    op.create_index('ix_designations_college_id', 'designations', ['college_id'])

    # 4. salary_components
    op.create_table(
        'salary_components',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('component_type', componenttype, nullable=False),
        sa.Column('is_default', sa.Boolean(), nullable=False, server_default=sa.text('false')),
        sa.Column('description', sa.String(500), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
    )
    op.create_index('ix_salary_components_id', 'salary_components', ['id'])

    # 5. employees
    op.create_table(
        'employees',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('employee_code', sa.String(50), nullable=False),
        sa.Column('first_name', sa.String(100), nullable=False),
        sa.Column('last_name', sa.String(100), nullable=False),
        sa.Column('email', sa.String(255), nullable=False),
        sa.Column('phone', sa.String(20), nullable=True),
        sa.Column('college_id', sa.Integer(), sa.ForeignKey('colleges.id'), nullable=False),
        sa.Column('department_id', sa.Integer(), sa.ForeignKey('departments.id'), nullable=False),
        sa.Column('designation_id', sa.Integer(), sa.ForeignKey('designations.id'), nullable=False),
        sa.Column('date_of_joining', sa.Date(), nullable=False),
        sa.Column('date_of_leaving', sa.Date(), nullable=True),
        sa.Column('bank_name', sa.String(255), nullable=True),
        sa.Column('bank_account_number', sa.String(50), nullable=True),
        sa.Column('ifsc_code', sa.String(20), nullable=True),
        sa.Column('pan_number', sa.String(20), nullable=True),
        sa.Column('ctc', sa.Numeric(12, 2), nullable=False),
        sa.Column('monthly_gross', sa.Numeric(12, 2), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.text('true')),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
    )
    op.create_index('ix_employees_id', 'employees', ['id'])
    op.create_index('ix_employees_employee_code', 'employees', ['employee_code'], unique=True)
    op.create_index('ix_employees_email', 'employees', ['email'])
    op.create_index('ix_employees_college_id', 'employees', ['college_id'])
    op.create_index('ix_employees_department_id', 'employees', ['department_id'])
    op.create_index('ix_employees_designation_id', 'employees', ['designation_id'])
    op.create_index('ix_employees_is_active', 'employees', ['is_active'])

    # 6. employee_salary_structures
    op.create_table(
        'employee_salary_structures',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('employee_id', sa.Integer(), sa.ForeignKey('employees.id'), nullable=False),
        sa.Column('salary_component_id', sa.Integer(), sa.ForeignKey('salary_components.id'), nullable=False),
        sa.Column('amount', sa.Numeric(12, 2), nullable=False),
        sa.Column('effective_from', sa.Date(), nullable=False),
        sa.Column('effective_to', sa.Date(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.UniqueConstraint('employee_id', 'salary_component_id', 'effective_from',
                            name='uq_employee_component_effective'),
    )
    op.create_index('ix_employee_salary_structures_id', 'employee_salary_structures', ['id'])
    op.create_index('ix_employee_salary_structures_employee_id', 'employee_salary_structures', ['employee_id'])
    op.create_index('ix_employee_salary_structures_salary_component_id', 'employee_salary_structures', ['salary_component_id'])

    # 7. leave_policies
    op.create_table(
        'leave_policies',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('college_id', sa.Integer(), sa.ForeignKey('colleges.id'), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('paid_leaves_per_year', sa.Integer(), nullable=False),
        sa.Column('max_carry_forward', sa.Integer(), nullable=False, server_default=sa.text('0')),
        sa.Column('comp_leave_enabled', sa.Boolean(), nullable=False, server_default=sa.text('true')),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
    )
    op.create_index('ix_leave_policies_id', 'leave_policies', ['id'])
    op.create_index('ix_leave_policies_college_id', 'leave_policies', ['college_id'])

    # 8. employee_leave_balances
    op.create_table(
        'employee_leave_balances',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('employee_id', sa.Integer(), sa.ForeignKey('employees.id'), nullable=False),
        sa.Column('year', sa.Integer(), nullable=False),
        sa.Column('paid_leaves_total', sa.Numeric(5, 2), nullable=False),
        sa.Column('paid_leaves_used', sa.Numeric(5, 2), nullable=False, server_default=sa.text('0')),
        sa.Column('comp_leaves_earned', sa.Numeric(5, 2), nullable=False, server_default=sa.text('0')),
        sa.Column('comp_leaves_used', sa.Numeric(5, 2), nullable=False, server_default=sa.text('0')),
        sa.Column('carry_forward_leaves', sa.Numeric(5, 2), nullable=False, server_default=sa.text('0')),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.UniqueConstraint('employee_id', 'year', name='uq_employee_year'),
    )
    op.create_index('ix_employee_leave_balances_id', 'employee_leave_balances', ['id'])
    op.create_index('ix_employee_leave_balances_employee_id', 'employee_leave_balances', ['employee_id'])
    op.create_index('ix_employee_leave_balances_year', 'employee_leave_balances', ['year'])

    # 9. attendance_uploads
    op.create_table(
        'attendance_uploads',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('college_id', sa.Integer(), sa.ForeignKey('colleges.id'), nullable=False),
        sa.Column('year', sa.Integer(), nullable=False),
        sa.Column('month', sa.Integer(), nullable=False),
        sa.Column('file_name', sa.String(255), nullable=False),
        sa.Column('file_path', sa.String(500), nullable=False),
        sa.Column('uploaded_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('status', uploadstatus, nullable=False, server_default='PENDING'),
        sa.Column('error_message', sa.String(1000), nullable=True),
        sa.Column('records_count', sa.Integer(), nullable=False, server_default=sa.text('0')),
    )
    op.create_index('ix_attendance_uploads_id', 'attendance_uploads', ['id'])
    op.create_index('ix_attendance_uploads_college_id', 'attendance_uploads', ['college_id'])
    op.create_index('ix_attendance_uploads_year', 'attendance_uploads', ['year'])
    op.create_index('ix_attendance_uploads_month', 'attendance_uploads', ['month'])

    # 10. attendance_records
    op.create_table(
        'attendance_records',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('employee_id', sa.Integer(), sa.ForeignKey('employees.id'), nullable=False),
        sa.Column('date', sa.Date(), nullable=False),
        sa.Column('status', attendancestatus, nullable=False),
        sa.Column('attendance_upload_id', sa.Integer(), sa.ForeignKey('attendance_uploads.id'), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.UniqueConstraint('employee_id', 'date', name='uq_employee_date'),
    )
    op.create_index('ix_attendance_records_id', 'attendance_records', ['id'])
    op.create_index('ix_attendance_records_employee_id', 'attendance_records', ['employee_id'])
    op.create_index('ix_attendance_records_date', 'attendance_records', ['date'])
    op.create_index('ix_attendance_records_attendance_upload_id', 'attendance_records', ['attendance_upload_id'])

    # 11. holidays
    op.create_table(
        'holidays',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('college_id', sa.Integer(), sa.ForeignKey('colleges.id'), nullable=False),
        sa.Column('date', sa.Date(), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('is_optional', sa.Boolean(), nullable=False, server_default=sa.text('false')),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.UniqueConstraint('college_id', 'date', name='uq_college_date'),
    )
    op.create_index('ix_holidays_id', 'holidays', ['id'])
    op.create_index('ix_holidays_college_id', 'holidays', ['college_id'])
    op.create_index('ix_holidays_date', 'holidays', ['date'])

    # 12. payroll_cycles
    op.create_table(
        'payroll_cycles',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('college_id', sa.Integer(), sa.ForeignKey('colleges.id'), nullable=False),
        sa.Column('year', sa.Integer(), nullable=False),
        sa.Column('month', sa.Integer(), nullable=False),
        sa.Column('total_working_days', sa.Integer(), nullable=False),
        sa.Column('status', payrollcyclestatus, nullable=False, server_default='DRAFT'),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('locked_at', sa.DateTime(), nullable=True),
        sa.UniqueConstraint('college_id', 'year', 'month', name='uq_college_year_month'),
    )
    op.create_index('ix_payroll_cycles_id', 'payroll_cycles', ['id'])
    op.create_index('ix_payroll_cycles_college_id', 'payroll_cycles', ['college_id'])
    op.create_index('ix_payroll_cycles_year', 'payroll_cycles', ['year'])
    op.create_index('ix_payroll_cycles_month', 'payroll_cycles', ['month'])

    # 13. payroll_entries
    op.create_table(
        'payroll_entries',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('payroll_cycle_id', sa.Integer(), sa.ForeignKey('payroll_cycles.id'), nullable=False),
        sa.Column('employee_id', sa.Integer(), sa.ForeignKey('employees.id'), nullable=False),
        sa.Column('days_present', sa.Numeric(5, 2), nullable=False),
        sa.Column('days_absent', sa.Numeric(5, 2), nullable=False),
        sa.Column('paid_leaves_used', sa.Numeric(5, 2), nullable=False, server_default=sa.text('0')),
        sa.Column('comp_leaves_used', sa.Numeric(5, 2), nullable=False, server_default=sa.text('0')),
        sa.Column('unpaid_leaves', sa.Numeric(5, 2), nullable=False, server_default=sa.text('0')),
        sa.Column('loss_of_pay', sa.Numeric(12, 2), nullable=False, server_default=sa.text('0')),
        sa.Column('gross_earnings', sa.Numeric(12, 2), nullable=False),
        sa.Column('total_deductions', sa.Numeric(12, 2), nullable=False),
        sa.Column('net_pay', sa.Numeric(12, 2), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.UniqueConstraint('payroll_cycle_id', 'employee_id', name='uq_cycle_employee'),
    )
    op.create_index('ix_payroll_entries_id', 'payroll_entries', ['id'])
    op.create_index('ix_payroll_entries_payroll_cycle_id', 'payroll_entries', ['payroll_cycle_id'])
    op.create_index('ix_payroll_entries_employee_id', 'payroll_entries', ['employee_id'])

    # 14. payroll_entry_components
    op.create_table(
        'payroll_entry_components',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('payroll_entry_id', sa.Integer(), sa.ForeignKey('payroll_entries.id'), nullable=False),
        sa.Column('salary_component_id', sa.Integer(), sa.ForeignKey('salary_components.id'), nullable=False),
        sa.Column('component_type', componenttype, nullable=False),
        sa.Column('amount', sa.Numeric(12, 2), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
    )
    op.create_index('ix_payroll_entry_components_id', 'payroll_entry_components', ['id'])
    op.create_index('ix_payroll_entry_components_payroll_entry_id', 'payroll_entry_components', ['payroll_entry_id'])
    op.create_index('ix_payroll_entry_components_salary_component_id', 'payroll_entry_components', ['salary_component_id'])

    # 15. payslips
    op.create_table(
        'payslips',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('payroll_entry_id', sa.Integer(), sa.ForeignKey('payroll_entries.id'), nullable=False, unique=True),
        sa.Column('employee_id', sa.Integer(), sa.ForeignKey('employees.id'), nullable=False),
        sa.Column('payroll_cycle_id', sa.Integer(), sa.ForeignKey('payroll_cycles.id'), nullable=False),
        sa.Column('file_path', sa.String(500), nullable=False),
        sa.Column('generated_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
    )
    op.create_index('ix_payslips_id', 'payslips', ['id'])
    op.create_index('ix_payslips_payroll_entry_id', 'payslips', ['payroll_entry_id'], unique=True)
    op.create_index('ix_payslips_employee_id', 'payslips', ['employee_id'])
    op.create_index('ix_payslips_payroll_cycle_id', 'payslips', ['payroll_cycle_id'])

    # 16. reports
    op.create_table(
        'reports',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('college_id', sa.Integer(), sa.ForeignKey('colleges.id'), nullable=True),
        sa.Column('year', sa.Integer(), nullable=False),
        sa.Column('month', sa.Integer(), nullable=False),
        sa.Column('report_type', sa.String(100), nullable=False),
        sa.Column('file_path', sa.String(500), nullable=False),
        sa.Column('generated_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
    )
    op.create_index('ix_reports_id', 'reports', ['id'])
    op.create_index('ix_reports_college_id', 'reports', ['college_id'])
    op.create_index('ix_reports_year', 'reports', ['year'])
    op.create_index('ix_reports_month', 'reports', ['month'])
    op.create_index('ix_reports_report_type', 'reports', ['report_type'])


def downgrade() -> None:
    op.drop_table('reports')
    op.drop_table('payslips')
    op.drop_table('payroll_entry_components')
    op.drop_table('payroll_entries')
    op.drop_table('payroll_cycles')
    op.drop_table('holidays')
    op.drop_table('attendance_records')
    op.drop_table('attendance_uploads')
    op.drop_table('employee_leave_balances')
    op.drop_table('leave_policies')
    op.drop_table('employee_salary_structures')
    op.drop_table('employees')
    op.drop_table('salary_components')
    op.drop_table('designations')
    op.drop_table('departments')
    op.drop_table('colleges')

    sa.Enum(name='payrollcyclestatus').drop(op.get_bind(), checkfirst=True)
    sa.Enum(name='attendancestatus').drop(op.get_bind(), checkfirst=True)
    sa.Enum(name='uploadstatus').drop(op.get_bind(), checkfirst=True)
    sa.Enum(name='componenttype').drop(op.get_bind(), checkfirst=True)
