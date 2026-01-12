'use client';

import { Card } from '@/components/ui/card';
import { EmployeeCard } from './EmployeeCard';
import { Employee } from '@/types/employee';

interface EmployeeListProps {
  employees: Employee[];
}

export function EmployeeList({ employees }: EmployeeListProps) {
  if (employees.length === 0) {
    return (
      <Card className="p-8 text-center">
        <p className="text-gray-500">Nenhum colaborador cadastrado ainda.</p>
      </Card>
    );
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      {employees.map((employee) => (
        <EmployeeCard key={employee.id} employee={employee} />
      ))}
    </div>
  );
}

