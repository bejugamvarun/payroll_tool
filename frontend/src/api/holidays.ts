import apiClient from './client';
import { Holiday, HolidayCreate } from '../types';

export const holidaysApi = {
  getAll: async (collegeId?: number, year?: number) => {
    const response = await apiClient.get<Holiday[]>('/holidays', {
      params: { college_id: collegeId, year },
    });
    return response.data;
  },

  create: async (data: HolidayCreate) => {
    const response = await apiClient.post<Holiday>('/holidays', data);
    return response.data;
  },

  delete: async (id: number) => {
    await apiClient.delete(`/holidays/${id}`);
  },

  bulkCreate: async (holidays: HolidayCreate[]) => {
    const response = await apiClient.post<Holiday[]>('/holidays/bulk', { holidays });
    return response.data;
  },
};
