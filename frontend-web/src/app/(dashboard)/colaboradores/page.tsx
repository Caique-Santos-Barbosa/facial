'use client';

import { useQuery } from '@tanstack/react-query';
import { useRouter } from 'next/navigation';
import { Button } from '@/components/ui/button';
import { colaboradoresApi } from '@/lib/api';
import { Plus } from 'lucide-react';
import { EmployeeList } from '@/components/employees/EmployeeList';

export default function ColaboradoresPage() {
  const router = useRouter();

  const { data: employees, isLoading } = useQuery({
    queryKey: ['employees'],
    queryFn: () => colaboradoresApi.list(),
  });

  return (
    <div className="p-8">
      <div className="flex justify-between items-center mb-8">
        <div>
          <h1 className="text-3xl font-bold text-slate-900">Colaboradores</h1>
          <p className="text-slate-500 mt-1">Gerencie os colaboradores do sistema</p>
        </div>
        <Button onClick={() => router.push('/colaboradores/novo')}>
          <Plus className="mr-2 h-4 w-4" />
          Novo Colaborador
        </Button>
      </div>

      {isLoading ? (
        <div className="text-center py-12">
          <p className="text-slate-500">Carregando colaboradores...</p>
        </div>
      ) : (
        <EmployeeList employees={employees || []} />
      )}
    </div>
  );
}
