'use client';

import { useQuery } from '@tanstack/react-query';
import { useRouter } from 'next/navigation';
import { Button } from '@/components/ui/button';
import { EmployeeList } from '@/components/employees/EmployeeList';
import { api } from '@/lib/api';
import { Plus } from 'lucide-react';

export default function ColaboradoresPage() {
  const router = useRouter();

  const { data: employees, isLoading } = useQuery({
    queryKey: ['employees'],
    queryFn: async () => {
      const response = await api.get('/employees');
      return response.data;
    },
  });

  return (
    <div>
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold">Colaboradores</h1>
        <Button onClick={() => router.push('/colaboradores/novo')}>
          <Plus className="mr-2 h-4 w-4" />
          Novo Colaborador
        </Button>
      </div>

      {isLoading ? (
        <p>Carregando...</p>
      ) : (
        <EmployeeList employees={employees || []} />
      )}
    </div>
  );
}

