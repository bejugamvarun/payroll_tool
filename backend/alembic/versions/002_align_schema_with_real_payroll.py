"""Align schema with real payroll Excel data

Revision ID: 002
Revises: 001
Create Date: 2026-03-01

Changes:
- employees: replace first_name/last_name with name, add staff_type enum,
  rename phone->mobile_number, add pay_scale/actual_basic/bank_branch/
  beneficiary_name/aadhaar_number, remove ctc/monthly_gross,
  make employee_code/email/department_id/designation_id nullable
- salary_components: add applies_to enum, is_percentage, percentage_value,
  percentage_of fields
- payroll_entries: rename unpaid_leaves->lop_days, add arrears column
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import ENUM as PgENUM


# revision identifiers, used by Alembic.
revision: str = '002'
down_revision: Union[str, None] = '001'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def create_enum_if_not_exists(name: str, *values: str) -> None:
    """Create a PostgreSQL enum type only if it doesn't already exist."""
    op.execute(f"""
        DO $$ BEGIN
            CREATE TYPE {name} AS ENUM ({', '.join(f"'{v}'" for v in values)});
        EXCEPTION WHEN duplicate_object THEN null;
        END $$;
    """)


def upgrade() -> None:
    # ------------------------------------------------------------------
    # 1. Create new enum types (idempotent)
    # ------------------------------------------------------------------
    create_enum_if_not_exists('stafftype', 'TEACHING', 'NON_TEACHING', 'SUB_STAFF')
    create_enum_if_not_exists('appliesto', 'ALL', 'TEACHING', 'NON_TEACHING', 'SUB_STAFF')

    # Bind enum handles that reference the already-created DB types.
    # create_type=False tells SQLAlchemy not to issue CREATE TYPE again.
    stafftype = PgENUM('TEACHING', 'NON_TEACHING', 'SUB_STAFF', name='stafftype', create_type=False)
    appliesto = PgENUM('ALL', 'TEACHING', 'NON_TEACHING', 'SUB_STAFF', name='appliesto', create_type=False)

    # ------------------------------------------------------------------
    # 2. employees table changes
    # ------------------------------------------------------------------

    # 2a. Add all new columns (temporarily nullable so existing rows are valid)
    op.add_column('employees', sa.Column('name', sa.String(255), nullable=True))
    op.add_column('employees', sa.Column('staff_type', stafftype, nullable=True))
    op.add_column('employees', sa.Column('mobile_number', sa.String(20), nullable=True))
    op.add_column('employees', sa.Column('pay_scale', sa.String(500), nullable=True))
    op.add_column('employees', sa.Column('actual_basic', sa.Numeric(12, 2), nullable=True))
    op.add_column('employees', sa.Column('bank_branch', sa.String(255), nullable=True))
    op.add_column('employees', sa.Column('beneficiary_name', sa.String(255), nullable=True))
    op.add_column('employees', sa.Column('aadhaar_number', sa.String(20), nullable=True))

    # 2b. Back-fill data from the old columns so we can enforce NOT NULL later
    op.execute(
        "UPDATE employees SET name = TRIM(first_name || ' ' || last_name) WHERE name IS NULL"
    )
    op.execute(
        "UPDATE employees SET mobile_number = phone WHERE mobile_number IS NULL"
    )
    op.execute(
        "UPDATE employees SET staff_type = 'TEACHING' WHERE staff_type IS NULL"
    )

    # 2c. Enforce NOT NULL on name and staff_type now that rows are populated
    op.alter_column('employees', 'name', nullable=False)
    op.alter_column('employees', 'staff_type', nullable=False)

    # 2d. Add index on staff_type for filtered queries
    op.create_index('ix_employees_staff_type', 'employees', ['staff_type'])

    # 2e. Relax constraints that the real data does not always supply
    op.alter_column('employees', 'employee_code', nullable=True)
    op.alter_column('employees', 'email', nullable=True)
    op.alter_column('employees', 'department_id', nullable=True)
    op.alter_column('employees', 'designation_id', nullable=True)

    # 2f. Drop columns that are no longer part of the real data model
    op.drop_column('employees', 'first_name')
    op.drop_column('employees', 'last_name')
    op.drop_column('employees', 'phone')
    op.drop_column('employees', 'ctc')
    op.drop_column('employees', 'monthly_gross')

    # ------------------------------------------------------------------
    # 3. salary_components table changes
    # ------------------------------------------------------------------

    # 3a. Add new columns (temporarily nullable)
    op.add_column('salary_components', sa.Column('applies_to', appliesto, nullable=True))
    op.add_column('salary_components', sa.Column('is_percentage', sa.Boolean(), nullable=True, server_default='false'))
    op.add_column('salary_components', sa.Column('percentage_value', sa.Numeric(5, 2), nullable=True))
    op.add_column('salary_components', sa.Column('percentage_of', sa.String(50), nullable=True))

    # 3b. Back-fill defaults for existing rows
    op.execute("UPDATE salary_components SET applies_to = 'ALL' WHERE applies_to IS NULL")
    op.execute("UPDATE salary_components SET is_percentage = false WHERE is_percentage IS NULL")

    # 3c. Enforce NOT NULL and remove server defaults (application layer owns defaults)
    op.alter_column('salary_components', 'applies_to', nullable=False, server_default=None)
    op.alter_column('salary_components', 'is_percentage', nullable=False, server_default=None)

    # ------------------------------------------------------------------
    # 4. payroll_entries table changes
    # ------------------------------------------------------------------

    # 4a. Rename unpaid_leaves to lop_days (same type, same semantics)
    op.alter_column('payroll_entries', 'unpaid_leaves', new_column_name='lop_days')

    # 4b. Add arrears column
    op.add_column('payroll_entries', sa.Column('arrears', sa.Numeric(12, 2), nullable=True, server_default='0'))
    op.execute("UPDATE payroll_entries SET arrears = 0 WHERE arrears IS NULL")
    op.alter_column('payroll_entries', 'arrears', nullable=False, server_default=None)


def downgrade() -> None:
    # ------------------------------------------------------------------
    # 4. payroll_entries - reverse
    # ------------------------------------------------------------------
    op.drop_column('payroll_entries', 'arrears')
    op.alter_column('payroll_entries', 'lop_days', new_column_name='unpaid_leaves')

    # ------------------------------------------------------------------
    # 3. salary_components - reverse
    # ------------------------------------------------------------------
    op.drop_column('salary_components', 'percentage_of')
    op.drop_column('salary_components', 'percentage_value')
    op.drop_column('salary_components', 'is_percentage')
    op.drop_column('salary_components', 'applies_to')

    # ------------------------------------------------------------------
    # 2. employees - reverse
    # ------------------------------------------------------------------
    # Re-add the old columns (nullable first, then we fill them)
    op.add_column('employees', sa.Column('first_name', sa.String(100), nullable=True))
    op.add_column('employees', sa.Column('last_name', sa.String(100), nullable=True))
    op.add_column('employees', sa.Column('phone', sa.String(20), nullable=True))
    op.add_column('employees', sa.Column('ctc', sa.Numeric(12, 2), nullable=True))
    op.add_column('employees', sa.Column('monthly_gross', sa.Numeric(12, 2), nullable=True))

    # Best-effort split of the single name field back into first/last
    op.execute(
        "UPDATE employees "
        "SET first_name = split_part(name, ' ', 1), "
        "    last_name  = CASE "
        "                   WHEN position(' ' in name) > 0 "
        "                   THEN substring(name from position(' ' in name) + 1) "
        "                   ELSE '' "
        "                 END"
    )

    # Drop the new index before dropping the column it covers
    op.drop_index('ix_employees_staff_type', table_name='employees')

    # Drop new columns
    op.drop_column('employees', 'aadhaar_number')
    op.drop_column('employees', 'beneficiary_name')
    op.drop_column('employees', 'bank_branch')
    op.drop_column('employees', 'actual_basic')
    op.drop_column('employees', 'pay_scale')
    op.drop_column('employees', 'mobile_number')
    op.drop_column('employees', 'staff_type')
    op.drop_column('employees', 'name')

    # Restore NOT NULL on previously relaxed columns
    op.alter_column('employees', 'designation_id', nullable=False)
    op.alter_column('employees', 'department_id', nullable=False)
    op.alter_column('employees', 'email', nullable=False)
    op.alter_column('employees', 'employee_code', nullable=False)

    # ------------------------------------------------------------------
    # 1. Drop enum types created in upgrade
    # ------------------------------------------------------------------
    op.execute('DROP TYPE IF EXISTS appliesto')
    op.execute('DROP TYPE IF EXISTS stafftype')
