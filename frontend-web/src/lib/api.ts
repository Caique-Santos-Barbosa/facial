import axios from 'axios';

const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor para adicionar token
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Interceptor para tratar erros
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('access_token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export { api };

// API Functions
export const authApi = {
  login: async (username: string, password: string) => {
    const response = await api.post('/auth/login', { username, password });
    return response.data;
  },
  
  me: async () => {
    const response = await api.get('/auth/me');
    return response.data;
  },
};

export const colaboradoresApi = {
  list: async (params?: { search?: string; active_only?: boolean }) => {
    const response = await api.get('/employees', { params });
    return response.data;
  },
  
  get: async (id: number) => {
    const response = await api.get(`/employees/${id}`);
    return response.data;
  },
  
  create: async (formData: FormData) => {
    const response = await api.post('/employees', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    return response.data;
  },
  
  update: async (id: number, data: any) => {
    const response = await api.put(`/employees/${id}`, data);
    return response.data;
  },
  
  delete: async (id: number) => {
    const response = await api.delete(`/employees/${id}`);
    return response.data;
  },
};

export const logsApi = {
  list: async (params?: {
    skip?: number;
    limit?: number;
    date_from?: string;
    date_to?: string;
    granted_only?: boolean;
  }) => {
    const response = await api.get('/access-logs', { params });
    return response.data;
  },
  
  stats: async (days: number = 7) => {
    const response = await api.get('/access-logs/stats', { params: { days } });
    return response.data;
  },
};