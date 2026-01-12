'use client';

import { useQuery } from '@tanstack/react-query';
import { AccessLogTable } from '@/components/access-logs/AccessLogTable';
import { api } from '@/lib/api';

export default function LogsAcessoPage() {
  const { data: logs, isLoading } = useQuery({
    queryKey: ['access-logs'],
    queryFn: async () => {
      const response = await api.get('/access/logs?limit=100');
      return response.data;
    },
  });

  return (
    <div>
      <h1 className="text-3xl font-bold mb-8">Logs de Acesso</h1>

      {isLoading ? (
        <p>Carregando...</p>
      ) : (
        <AccessLogTable logs={logs || []} />
      )}
    </div>
  );
}

