import apiClient from './client';
import { Payslip } from '../types';

export const payslipsApi = {
  generateForCycle: async (cycleId: number) => {
    const response = await apiClient.post(`/payslips/generate/${cycleId}`);
    return response.data;
  },

  getForCycle: async (cycleId?: number, employeeId?: number) => {
    const response = await apiClient.get<Payslip[]>('/payslips', {
      params: { payroll_cycle_id: cycleId, employee_id: employeeId },
    });
    return response.data;
  },

  downloadSingle: async (payslipId: number) => {
    const response = await apiClient.get(`/payslips/${payslipId}/download`, {
      responseType: 'blob',
    });
    return response.data;
  },

  downloadBulk: async (cycleId: number) => {
    const response = await apiClient.get(`/payslips/download-bulk/${cycleId}`, {
      responseType: 'blob',
    });
    return response.data;
  },
};
