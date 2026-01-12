'use client';

import { useQuery } from '@tanstack/react-query';
import { api } from '@/lib/api';
import { Card } from '@/components/ui/card';

export default function DashboardPage() {
  const { data: stats } = useQuery({
    queryKey: ['access-stats'],
    queryFn: async () => {
      const response = await api.get('/access/stats?days=7');
      return response.data;
    },
  });

  return (
    <div>
      <h1 className="text-3xl font-bold mb-8">Dashboard</h1>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Card className="p-6">
          <h3 className="text-sm font-medium text-gray-600">Tentativas (7 dias)</h3>
          <p className="text-3xl font-bold mt-2">{stats?.total_attempts || 0}</p>
        </Card>

        <Card className="p-6">
          <h3 className="text-sm font-medium text-gray-600">Acessos Permitidos</h3>
          <p className="text-3xl font-bold mt-2 text-green-600">{stats?.granted || 0}</p>
        </Card>

        <Card className="p-6">
          <h3 className="text-sm font-medium text-gray-600">Taxa de Sucesso</h3>
          <p className="text-3xl font-bold mt-2">{stats?.success_rate || 0}%</p>
        </Card>
      </div>
    </div>
  );
}

