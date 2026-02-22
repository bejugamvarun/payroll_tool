import apiClient from './client';
import {
  Employee,
  EmployeeCreate,
  EmployeeUpdate,
  EmployeeSalaryStructure,
  SalaryStructureCreate,
  EmployeeLeaveBalance,
  AttendanceRecord,
} from '../types';

export const employeesApi = {
  getAll: async (skip = 0, limit = 100, collegeId?: number, departmentId?: number, isActive?: boolean) => {
    const response = await apiClient.get<Employee[]>('/employees', {
      params: {
        skip,
        limit,
        college_id: collegeId,
        department_id: departmentId,
        is_active: isActive,
      },
    });
    return response.data;
  },

  getById: async (id: number) => {
    const response = await apiClient.get<Employee>(`/employees/${id}`);
    return response.data;
  },

  create: async (data: EmployeeCreate) => {
    const response = await apiClient.post<Employee>('/employees', data);
    return response.data;
  },

  update: async (id: number, data: EmployeeUpdate) => {
    const response = await apiClient.put<Employee>(`/employees/${id}`, data);
    return response.data;
  },

  delete: async (id: number) => {
    await apiClient.delete(`/employees/${id}`);
  },

  bulkUpload: async (file: File, collegeId: number) => {
    const formData = new FormData();
    formData.append('file', file);
    const response = await apiClient.post(
      `/employees/upload-excel?college_id=${collegeId}`,
      formData,
      { headers: { 'Content-Type': 'multipart/form-data' } }
    );
    return response.data;
  },

  getSalaryStructure: async (employeeId: number) => {
    const response = await apiClient.get<EmployeeSalaryStructure[]>(
      `/employees/${employeeId}/salary-structure`
    );
    return response.data;
  },

  updateSalaryStructure: async (employeeId: number, structures: SalaryStructureCreate[]) => {
    const response = await apiClient.put<EmployeeSalaryStructure[]>(
      `/employees/${employeeId}/salary-structure`,
      { structures }
    );
    return response.data;
  },

  getLeaveBalance: async (employeeId: number, year?: number) => {
    const response = await apiClient.get<EmployeeLeaveBalance>(
      `/employees/${employeeId}/leave-balance`,
      { params: { year } }
    );
    return response.data;
  },

  getAttendanceHistory: async (employeeId: number, year?: number, month?: number) => {
    const response = await apiClient.get<AttendanceRecord[]>(
      `/employees/${employeeId}/attendance`,
      { params: { year, month } }
    );
    return response.data;
  },
};
