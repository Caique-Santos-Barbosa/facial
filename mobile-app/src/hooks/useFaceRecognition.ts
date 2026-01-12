import { useState, useCallback } from 'react';
import { recognizeFace } from '../services/api';
import { getDeviceId } from '../services/storage';

export interface RecognitionState {
  processing: boolean;
  result: any | null;
  error: string | null;
}

export function useFaceRecognition() {
  const [state, setState] = useState<RecognitionState>({
    processing: false,
    result: null,
    error: null,
  });

  const recognize = useCallback(async (imageUri: string) => {
    setState({ processing: true, result: null, error: null });

    try {
      const deviceId = await getDeviceId();
      const result = await recognizeFace(imageUri);
      
      setState({ processing: false, result, error: null });
      
      // Auto-reset após 5 segundos
      setTimeout(() => {
        setState({ processing: false, result: null, error: null });
      }, 5000);
      
      return result;
    } catch (error: any) {
      const errorMessage = error.response?.data?.detail || 'Erro ao reconhecer face';
      setState({ processing: false, result: null, error: errorMessage });
      throw error;
    }
  }, []);

  const reset = useCallback(() => {
    setState({ processing: false, result: null, error: null });
  }, []);

  return {
    ...state,
    recognize,
    reset,
  };
}

