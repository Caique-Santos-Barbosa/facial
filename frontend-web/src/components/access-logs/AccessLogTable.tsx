'use client';

import { Card } from '@/components/ui/card';
import { AccessLog } from '@/types/access';

interface AccessLogTableProps {
  logs: AccessLog[];
}

export function AccessLogTable({ logs }: AccessLogTableProps) {
  if (logs.length === 0) {
    return (
      <Card className="p-8 text-center">
        <p className="text-gray-500">Nenhum log de acesso encontrado.</p>
      </Card>
    );
  }

  return (
    <Card>
      <div className="overflow-x-auto">
        <table className="w-full">
          <thead>
            <tr className="border-b">
              <th className="text-left p-4">Data/Hora</th>
              <th className="text-left p-4">Colaborador</th>
              <th className="text-left p-4">Status</th>
              <th className="text-left p-4">Confiança</th>
              <th className="text-left p-4">Liveness</th>
              <th className="text-left p-4">Motivo</th>
            </tr>
          </thead>
          <tbody>
            {logs.map((log) => (
              <tr key={log.id} className="border-b">
                <td className="p-4">
                  {new Date(log.attempted_at).toLocaleString('pt-BR')}
                </td>
                <td className="p-4">
                  {log.employee?.full_name || 'Desconhecido'}
                </td>
                <td className="p-4">
                  <span
                    className={`px-2 py-1 rounded ${
                      log.access_granted
                        ? 'bg-green-100 text-green-800'
                        : 'bg-red-100 text-red-800'
                    }`}
                  >
                    {log.access_granted ? 'Permitido' : 'Negado'}
                  </span>
                </td>
                <td className="p-4">
                  {log.confidence_score
                    ? `${(log.confidence_score * 100).toFixed(1)}%`
                    : '-'}
                </td>
                <td className="p-4">
                  {log.liveness_passed !== null
                    ? log.liveness_passed
                      ? '✓'
                      : '✗'
                    : '-'}
                </td>
                <td className="p-4 text-sm text-gray-600">
                  {log.denial_reason || '-'}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </Card>
  );
}

