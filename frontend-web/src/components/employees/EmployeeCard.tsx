'use client';

import { Card } from '@/components/ui/card';
import { Employee } from '@/types/employee';
import { Badge } from '@/components/ui/badge';

interface EmployeeCardProps {
  employee: Employee;
}

export function EmployeeCard({ employee }: EmployeeCardProps) {
  return (
    <Card className="p-6">
      <div className="flex items-start justify-between mb-4">
        <div>
          <h3 className="text-lg font-semibold">{employee.full_name}</h3>
          <p className="text-sm text-gray-600">{employee.email}</p>
        </div>
        <Badge variant={employee.is_active ? 'default' : 'secondary'}>
          {employee.is_active ? 'Ativo' : 'Inativo'}
        </Badge>
      </div>

      <div className="space-y-2 text-sm">
        {employee.department && (
          <p>
            <span className="font-medium">Departamento:</span> {employee.department}
          </p>
        )}
        {employee.position && (
          <p>
            <span className="font-medium">Cargo:</span> {employee.position}
          </p>
        )}
        {employee.phone && (
          <p>
            <span className="font-medium">Telefone:</span> {employee.phone}
          </p>
        )}
      </div>
    </Card>
  );
}

