'use client';

import { useQuery } from '@tanstack/react-query';
import { colaboradoresApi } from '@/lib/api';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card } from '@/components/ui/card';
import { Plus, Search, Users } from 'lucide-react';
import Link from 'next/link';
import { useState } from 'react';
import { Avatar, AvatarFallback } from '@/components/ui/avatar';
import { Badge } from '@/components/ui/badge';

export default function ColaboradoresPage() {
  const [search, setSearch] = useState('');

  const { data: colaboradores, isLoading } = useQuery({
    queryKey: ['colaboradores', search],
    queryFn: () => colaboradoresApi.list({ search, active_only: true }),
  });

  return (
    <div className="p-8">
      {/* Header */}
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-3xl font-bold text-slate-900">Colaboradores</h1>
          <p className="text-slate-500 mt-1">
            Gerencie os colaboradores com reconhecimento facial
          </p>
        </div>
        <Link href="/colaboradores/novo">
          <Button>
            <Plus className="mr-2 h-4 w-4" />
            Novo Colaborador
          </Button>
        </Link>
      </div>

      {/* Search */}
      <div className="mb-6">
        <div className="relative max-w-md">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-slate-400" />
          <Input
            placeholder="Buscar por nome, CPF ou email..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="pl-10"
          />
        </div>
      </div>

      {/* Lista */}
      {isLoading ? (
        <div className="text-center py-12">
          <div className="inline-block h-8 w-8 animate-spin rounded-full border-4 border-solid border-green-500 border-r-transparent"></div>
          <p className="mt-4 text-slate-500">Carregando...</p>
        </div>
      ) : colaboradores && colaboradores.length > 0 ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {colaboradores.map((colaborador: any) => (
            <Link key={colaborador.id} href={`/colaboradores/${colaborador.id}`}>
              <Card className="p-6 hover:shadow-lg transition-shadow cursor-pointer">
                <div className="flex items-start gap-4">
                  <Avatar className="h-16 w-16">
                    <AvatarFallback className="bg-green-100 text-green-700 text-xl font-semibold">
                      {colaborador.full_name.charAt(0)}
                    </AvatarFallback>
                  </Avatar>
                  
                  <div className="flex-1 min-w-0">
                    <h3 className="font-semibold text-slate-900 truncate">
                      {colaborador.full_name}
                    </h3>
                    <p className="text-sm text-slate-500 truncate">
                      {colaborador.email}
                    </p>
                    
                    {colaborador.department && (
                      <div className="mt-2">
                        <Badge variant="secondary">
                          {colaborador.department}
                        </Badge>
                      </div>
                    )}
                    
                    <div className="mt-3 flex items-center text-xs text-slate-400">
                      <Users className="h-3 w-3 mr-1" />
                      Cadastrado em {new Date(colaborador.created_at).toLocaleDateString('pt-BR')}
                    </div>
                  </div>
                </div>
              </Card>
            </Link>
          ))}
        </div>
      ) : (
        <Card className="p-12 text-center">
          <Users className="h-12 w-12 text-slate-300 mx-auto mb-4" />
          <h3 className="text-lg font-semibold text-slate-900 mb-2">
            Nenhum colaborador encontrado
          </h3>
          <p className="text-slate-500 mb-6">
            {search ? 'Tente buscar por outro termo' : 'Comece cadastrando seu primeiro colaborador'}
          </p>
          {!search && (
            <Link href="/colaboradores/novo">
              <Button>
                <Plus className="mr-2 h-4 w-4" />
                Cadastrar Primeiro Colaborador
              </Button>
            </Link>
          )}
        </Card>
      )}
    </div>
  );
}
