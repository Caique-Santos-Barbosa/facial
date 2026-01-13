'use client';

import { useQuery } from '@tanstack/react-query';
import { logsApi, colaboradoresApi } from '@/lib/api';
import { Card, CardContent } from '@/components/ui/card';
import { Users, CheckCircle, XCircle, Activity } from 'lucide-react';

export default function DashboardPage() {
  const { data: stats } = useQuery({
    queryKey: ['stats'],
    queryFn: () => logsApi.stats(7),
  });

  const { data: colaboradores } = useQuery({
    queryKey: ['colaboradores'],
    queryFn: () => colaboradoresApi.list({ active_only: true }),
  });

  const statsCards = [
    {
      title: 'Colaboradores Ativos',
      value: colaboradores?.length || 0,
      icon: Users,
      color: 'text-blue-500',
      bgColor: 'bg-blue-50',
    },
    {
      title: 'Acessos Permitidos',
      value: stats?.granted || 0,
      icon: CheckCircle,
      color: 'text-green-500',
      bgColor: 'bg-green-50',
    },
    {
      title: 'Acessos Negados',
      value: stats?.denied || 0,
      icon: XCircle,
      color: 'text-red-500',
      bgColor: 'bg-red-50',
    },
    {
      title: 'Taxa de Sucesso',
      value: `${stats?.success_rate || 0}%`,
      icon: Activity,
      color: 'text-purple-500',
      bgColor: 'bg-purple-50',
    },
  ];

  return (
    <div className="p-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-slate-900">Dashboard</h1>
        <p className="text-slate-500 mt-1">
          Visão geral do sistema de reconhecimento facial
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {statsCards.map((card) => {
          const Icon = card.icon;
          return (
            <Card key={card.title}>
              <CardContent className="p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm font-medium text-slate-500">{card.title}</p>
                    <p className="text-3xl font-bold text-slate-900 mt-2">{card.value}</p>
                  </div>
                  <div className={`${card.bgColor} p-3 rounded-full`}>
                    <Icon className={`h-6 w-6 ${card.color}`} />
                  </div>
                </div>
              </CardContent>
            </Card>
          );
        })}
      </div>
    </div>
  );
}
