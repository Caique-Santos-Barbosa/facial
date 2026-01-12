import axios from 'axios';

const API_URL = process.env.EXPO_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

export const api = axios.create({
  baseURL: API_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'multipart/form-data',
  },
});

export interface RecognitionResponse {
  success: boolean;
  access_granted: boolean;
  employee?: {
    id: number;
    name: string;
    department?: string;
    position?: string;
  };
  confidence?: number;
  message: string;
  timestamp?: string;
  liveness_details?: any;
}

export async function recognizeFace(imageUri: string): Promise<RecognitionResponse> {
  const formData = new FormData();
  
  formData.append('image', {
    uri: imageUri,
    type: 'image/jpeg',
    name: 'face.jpg',
  } as any);

  const response = await api.post<RecognitionResponse>('/recognition/recognize', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });

  return response.data;
}

