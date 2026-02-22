// Base types
export interface PaginatedResponse<T> {
  items: T[];
  total: number;
}

// College types
export interface College {
  id: number;
  serial_number: number;
  college_code: string;
  name: string;
  address?: string;
  created_at: string;
  updated_at: string;
}

export interface CollegeCreate {
  serial_number: number;
  college_code: string;
  name: string;
  address?: string;
}

// Department types
export interface Department {
  id: number;
  name: string;
  college_id: number;
  created_at: string;
}

export interface DepartmentCreate {
  name: string;
  college_id: number;
}

// Designation types
export interface Designation {
  id: number;
  name: string;
  college_id?: number;
  created_at: string;
}

export interface DesignationCreate {
  name: string;
  college_id?: number;
}

// Salary Component types
export type ComponentType = 'EARNING' | 'DEDUCTION';

export interface SalaryComponent {
  id: number;
  name: string;
  component_type: ComponentType;
  is_default: boolean;
  description?: string;
  created_at: string;
}

export interface SalaryComponentCreate {
  name: string;
  component_type: ComponentType;
  is_default?: boolean;
  description?: string;
}

// Employee types
export interface Employee {
  id: number;
  employee_code: string;
  first_name: string;
  last_name: string;
  email: string;
  phone?: string;
  college_id: number;
  department_id: number;
  designation_id: number;
  date_of_joining: string;
  date_of_leaving?: string;
  bank_name?: string;
  bank_account_number?: string;
  ifsc_code?: string;
  pan_number?: string;
  ctc: number;
  monthly_gross: number;
  is_active: boolean;
  college_name?: string;
  department_name?: string;
  designation_name?: string;
  created_at: string;
  updated_at: string;
}

export interface EmployeeCreate {
  employee_code: string;
  first_name: string;
  last_name: string;
  email: string;
  phone?: string;
  college_id: number;
  department_id: number;
  designation_id: number;
  date_of_joining: string;
  date_of_leaving?: string;
  bank_name?: string;
  bank_account_number?: string;
  ifsc_code?: string;
  pan_number?: string;
  ctc: number;
  monthly_gross: number;
  is_active?: boolean;
}

export interface EmployeeUpdate {
  first_name?: string;
  last_name?: string;
  email?: string;
  phone?: string;
  department_id?: number;
  designation_id?: number;
  date_of_leaving?: string;
  bank_name?: string;
  bank_account_number?: string;
  ifsc_code?: string;
  pan_number?: string;
  ctc?: number;
  monthly_gross?: number;
  is_active?: boolean;
}

// Salary Structure types
export interface EmployeeSalaryStructure {
  id: number;
  employee_id: number;
  salary_component_id: number;
  amount: number;
  effective_from: string;
  effective_to?: string;
  created_at: string;
  component_name?: string;
  component_type?: ComponentType;
}

export interface SalaryStructureCreate {
  salary_component_id: number;
  amount: number;
  effective_from: string;
  effective_to?: string;
}

// Leave Policy types
export interface LeavePolicy {
  id: number;
  name: string;
  college_id: number;
  paid_leaves_per_year: number;
  max_carry_forward: number;
  comp_leave_enabled: boolean;
  created_at: string;
}

export interface LeavePolicyCreate {
  name: string;
  college_id: number;
  paid_leaves_per_year: number;
  max_carry_forward?: number;
  comp_leave_enabled?: boolean;
}

// Employee Leave Balance types
export interface EmployeeLeaveBalance {
  id: number;
  employee_id: number;
  year: number;
  paid_leaves_total: number;
  paid_leaves_used: number;
  comp_leaves_earned: number;
  comp_leaves_used: number;
  carry_forward_leaves: number;
  created_at: string;
  updated_at: string;
}

export interface LeaveBalanceCreate {
  employee_id: number;
  year: number;
  paid_leaves_total: number;
  paid_leaves_used?: number;
  comp_leaves_earned?: number;
  comp_leaves_used?: number;
  carry_forward_leaves?: number;
}

// Attendance types
export type AttendanceStatus = 'PRESENT' | 'ABSENT' | 'HALF_DAY' | 'WEEKEND_WORK' | 'HOLIDAY' | 'LEAVE';

export interface AttendanceUpload {
  id: number;
  college_id: number;
  year: number;
  month: number;
  file_name: string;
  file_path: string;
  uploaded_at: string;
  status: 'PENDING' | 'PROCESSING' | 'COMPLETED' | 'FAILED';
  error_message?: string;
  records_count: number;
}

export interface AttendanceRecord {
  id: number;
  employee_id: number;
  date: string;
  status: AttendanceStatus;
  attendance_upload_id?: number;
  created_at: string;
}

export interface AttendanceSummary {
  employee_id: number;
  employee_name: string;
  total_days: number;
  present_days: number;
  absent_days: number;
  half_days: number;
  weekend_work_days: number;
  holidays: number;
  leaves: number;
}

// Holiday types
export interface Holiday {
  id: number;
  name: string;
  date: string;
  college_id: number;
  is_optional: boolean;
  created_at: string;
}

export interface HolidayCreate {
  name: string;
  date: string;
  college_id: number;
  is_optional?: boolean;
}

// Payroll types
export type PayrollStatus = 'DRAFT' | 'PROCESSING' | 'COMPLETED' | 'LOCKED';

export interface PayrollCycle {
  id: number;
  college_id: number;
  year: number;
  month: number;
  total_working_days: number;
  status: PayrollStatus;
  created_at: string;
  updated_at: string;
  locked_at?: string;
  college_name?: string;
}

export interface PayrollEntry {
  id: number;
  payroll_cycle_id: number;
  employee_id: number;
  days_present: number;
  days_absent: number;
  paid_leaves_used: number;
  comp_leaves_used: number;
  unpaid_leaves: number;
  loss_of_pay: number;
  gross_earnings: number;
  total_deductions: number;
  net_pay: number;
  created_at: string;
  employee_name?: string;
  employee_code?: string;
  components?: PayrollEntryComponent[];
}

export interface PayrollEntryComponent {
  id: number;
  payroll_entry_id: number;
  salary_component_id: number;
  component_type: ComponentType;
  amount: number;
  created_at: string;
  component_name?: string;
}

export interface PayrollCalculateRequest {
  college_id?: number;
  year: number;
  month: number;
  employee_ids?: number[];
}

// Payslip types
export interface Payslip {
  id: number;
  payroll_entry_id: number;
  employee_id: number;
  payroll_cycle_id: number;
  file_path: string;
  generated_at: string;
  employee_name?: string;
  employee_code?: string;
}

// Report types
export interface Report {
  id: number;
  college_id?: number;
  year: number;
  month: number;
  report_type: string;
  file_path: string;
  generated_at: string;
  college_name?: string;
}

export interface ReportGenerateRequest {
  college_id?: number;
  year: number;
  month: number;
  report_type: string;
}
