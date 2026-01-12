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

