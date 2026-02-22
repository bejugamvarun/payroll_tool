import apiClient from './client';
import { College, CollegeCreate } from '../types';

export const collegesApi = {
  getAll: async (skip = 0, limit = 100) => {
    const response = await apiClient.get<College[]>('/colleges', {
      params: { skip, limit },
    });
    return response.data;
  },

  getById: async (id: number) => {
    const response = await apiClient.get<College>(`/colleges/${id}`);
    return response.data;
  },

  create: async (data: CollegeCreate) => {
    const response = await apiClient.post<College>('/colleges', data);
    return response.data;
  },

  update: async (id: number, data: Partial<CollegeCreate>) => {
    const response = await apiClient.put<College>(`/colleges/${id}`, data);
    return response.data;
  },

  delete: async (id: number) => {
    await apiClient.delete(`/colleges/${id}`);
  },

  bulkCreate: async (colleges: CollegeCreate[]) => {
    const response = await apiClient.post<College[]>('/colleges/bulk', { colleges });
    return response.data;
  },
};
