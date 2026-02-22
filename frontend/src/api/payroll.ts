import apiClient from './client';
import { PayrollCycle, PayrollEntry } from '../types';

export const payrollApi = {
  getCycles: async (collegeId?: number, year?: number, month?: number) => {
    const response = await apiClient.get<PayrollCycle[]>('/payroll/cycles', {
      params: { college_id: collegeId, year, month },
    });
    return response.data;
  },

  getCycleById: async (cycleId: number) => {
    const response = await apiClient.get<PayrollCycle>(`/payroll/cycles/${cycleId}`);
    return response.data;
  },

  calculate: async (collegeId: number, year: number, month: number) => {
    const response = await apiClient.post<PayrollCycle>('/payroll/calculate', {
      college_id: collegeId,
      year,
      month,
    });
    return response.data;
  },

  getEntries: async (cycleId?: number, employeeId?: number) => {
    const response = await apiClient.get<PayrollEntry[]>('/payroll/entries', {
      params: { payroll_cycle_id: cycleId, employee_id: employeeId },
    });
    return response.data;
  },

  lockCycle: async (cycleId: number) => {
    const response = await apiClient.post<PayrollCycle>(`/payroll/cycles/${cycleId}/lock`);
    return response.data;
  },
};
