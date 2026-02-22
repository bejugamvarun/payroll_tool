import apiClient from './client';
import { LeavePolicy, LeavePolicyCreate } from '../types';

export const leavePoliciesApi = {
  getAll: async (skip = 0, limit = 100, collegeId?: number) => {
    const response = await apiClient.get<LeavePolicy[]>('/leave-policies', {
      params: { skip, limit, college_id: collegeId },
    });
    return response.data;
  },

  create: async (data: LeavePolicyCreate) => {
    const response = await apiClient.post<LeavePolicy>('/leave-policies', data);
    return response.data;
  },

  update: async (id: number, data: Partial<LeavePolicyCreate>) => {
    const response = await apiClient.put<LeavePolicy>(`/leave-policies/${id}`, data);
    return response.data;
  },

  delete: async (id: number) => {
    await apiClient.delete(`/leave-policies/${id}`);
  },
};
