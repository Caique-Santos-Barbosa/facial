import { Employee } from './employee';

export interface AccessLog {
  id: number;
  employee_id?: number;
  employee?: Employee;
  access_granted: boolean;
  confidence_score?: number;
  liveness_passed?: boolean;
  attempted_at: string;
  device_id?: string;
  device_location?: string;
  denial_reason?: string;
}

