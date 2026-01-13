import axios from 'axios';
import { API_URL } from '../constants/config';

const api = axios.create({
  baseURL: API_URL,
  timeout: 30000,
});

export const recognizeFace = async (formData: FormData) => {
  const response = await api.post('/recognition/recognize', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  return response.data;
};

export default api;
