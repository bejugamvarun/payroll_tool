import apiClient from './client';
import { SalaryComponent, SalaryComponentCreate } from '../types';

export const salaryComponentsApi = {
  getAll: async (skip = 0, limit = 100) => {
    const response = await apiClient.get<SalaryComponent[]>('/salary-components', {
      params: { skip, limit },
    });
    return response.data;
  },

  create: async (data: SalaryComponentCreate) => {
    const response = await apiClient.post<SalaryComponent>('/salary-components', data);
    return response.data;
  },

  update: async (id: number, data: Partial<SalaryComponentCreate>) => {
    const response = await apiClient.put<SalaryComponent>(`/salary-components/${id}`, data);
    return response.data;
  },

  delete: async (id: number) => {
    await apiClient.delete(`/salary-components/${id}`);
  },
};
