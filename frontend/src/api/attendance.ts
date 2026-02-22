import apiClient from './client';
import { AttendanceUpload, AttendanceRecord, AttendanceSummary } from '../types';

export const attendanceApi = {
  upload: async (file: File, collegeId: number, year: number, month: number) => {
    const formData = new FormData();
    formData.append('file', file);
    const response = await apiClient.post<AttendanceUpload>(
      `/attendance/upload?college_id=${collegeId}&year=${year}&month=${month}`,
      formData,
      { headers: { 'Content-Type': 'multipart/form-data' } }
    );
    return response.data;
  },

  getUploads: async (collegeId?: number, year?: number, month?: number) => {
    const response = await apiClient.get<AttendanceUpload[]>('/attendance/uploads', {
      params: { college_id: collegeId, year, month },
    });
    return response.data;
  },

  getRecords: async (employeeId?: number, year?: number, month?: number, skip = 0, limit = 100) => {
    const response = await apiClient.get<AttendanceRecord[]>('/attendance/records', {
      params: { employee_id: employeeId, year, month, skip, limit },
    });
    return response.data;
  },

  getSummary: async (collegeId: number, year: number, month: number) => {
    const response = await apiClient.get<AttendanceSummary[]>('/attendance/summary', {
      params: { college_id: collegeId, year, month },
    });
    return response.data;
  },
};
