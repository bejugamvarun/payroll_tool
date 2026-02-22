import apiClient from './client';
import { Report, ReportGenerateRequest } from '../types';

export const reportsApi = {
  generate: async (data: ReportGenerateRequest) => {
    const response = await apiClient.post<Report>('/reports/generate', data);
    return response.data;
  },

  getAll: async (collegeId?: number, year?: number, month?: number) => {
    const response = await apiClient.get<Report[]>('/reports', {
      params: { college_id: collegeId, year, month },
    });
    return response.data;
  },

  download: async (reportId: number) => {
    const response = await apiClient.get(`/reports/${reportId}/download`, {
      responseType: 'blob',
    });
    return response.data;
  },
};
