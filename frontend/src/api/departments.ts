import apiClient from './client';
import { Department, DepartmentCreate } from '../types';

export const departmentsApi = {
  getByCollege: async (collegeId: number) => {
    const response = await apiClient.get<Department[]>('/departments', {
      params: { college_id: collegeId },
    });
    return response.data;
  },

  create: async (data: DepartmentCreate) => {
    const response = await apiClient.post<Department>('/departments', data);
    return response.data;
  },

  delete: async (id: number) => {
    await apiClient.delete(`/departments/${id}`);
  },
};
