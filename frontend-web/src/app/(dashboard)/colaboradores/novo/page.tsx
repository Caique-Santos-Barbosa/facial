'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import * as z from 'zod';
import { toast } from 'sonner';
import { colaboradoresApi } from '@/lib/api';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { FaceCapture } from '@/components/colaboradores/FaceCapture';
import { ArrowLeft } from 'lucide-react';
import Link from 'next/link';

const colaboradorSchema = z.object({
  full_name: z.string().min(3, 'Nome deve ter no mínimo 3 caracteres'),
  cpf: z.string().min(11, 'CPF inválido'),
  email: z.string().email('Email inválido'),
  phone: z.string().optional(),
  department: z.string().optional(),
  position: z.string().optional(),
});

type ColaboradorForm = z.infer<typeof colaboradorSchema>;

export default function NovoColaboradorPage() {
  const router = useRouter();
  const [loading, setLoading] = useState(false);
  const [faceImage, setFaceImage] = useState<File | null>(null);

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<ColaboradorForm>({
    resolver: zodResolver(colaboradorSchema),
  });

  const onSubmit = async (data: ColaboradorForm) => {
    if (!faceImage) {
      toast.error('Por favor, capture uma foto do rosto');
      return;
    }

    setLoading(true);

    try {
      const formData = new FormData();
      
      Object.entries(data).forEach(([key, value]) => {
        if (value) formData.append(key, value);
      });
      
      formData.append('face_image', faceImage);

      await colaboradoresApi.create(formData);

      toast.success('Colaborador cadastrado com sucesso!');
      router.push('/colaboradores');
    } catch (error: any) {
      toast.error(error.response?.data?.detail || 'Erro ao cadastrar colaborador');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-8">
      {/* Header */}
      <div className="mb-8">
        <Link
          href="/colaboradores"
          className="inline-flex items-center text-sm text-slate-500 hover:text-slate-700 mb-4"
        >
          <ArrowLeft className="h-4 w-4 mr-2" />
          Voltar para colaboradores
        </Link>
        <h1 className="text-3xl font-bold text-slate-900">Novo Colaborador</h1>
        <p className="text-slate-500 mt-1">
          Cadastre um novo colaborador com reconhecimento facial
        </p>
      </div>

      <Card className="max-w-4xl">
        <CardHeader>
          <CardTitle>Dados do Colaborador</CardTitle>
          <CardDescription>
            Preencha os dados e capture uma foto do rosto
          </CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
            {/* Dados Pessoais */}
            <div className="space-y-4">
              <h3 className="text-lg font-semibold">Dados Pessoais</h3>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="full_name">Nome Completo *</Label>
                  <Input
                    id="full_name"
                    {...register('full_name')}
                    disabled={loading}
                  />
                  {errors.full_name && (
                    <p className="text-sm text-red-500">{errors.full_name.message}</p>
                  )}
                </div>

                <div className="space-y-2">
                  <Label htmlFor="cpf">CPF *</Label>
                  <Input
                    id="cpf"
                    placeholder="000.000.000-00"
                    {...register('cpf')}
                    disabled={loading}
                  />
                  {errors.cpf && (
                    <p className="text-sm text-red-500">{errors.cpf.message}</p>
                  )}
                </div>

                <div className="space-y-2">
                  <Label htmlFor="email">Email *</Label>
                  <Input
                    id="email"
                    type="email"
                    {...register('email')}
                    disabled={loading}
                  />
                  {errors.email && (
                    <p className="text-sm text-red-500">{errors.email.message}</p>
                  )}
                </div>

                <div className="space-y-2">
                  <Label htmlFor="phone">Telefone</Label>
                  <Input
                    id="phone"
                    placeholder="(00) 00000-0000"
                    {...register('phone')}
                    disabled={loading}
                  />
                </div>
              </div>
            </div>

            {/* Dados Profissionais */}
            <div className="space-y-4">
              <h3 className="text-lg font-semibold">Dados Profissionais</h3>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="department">Departamento</Label>
                  <Input
                    id="department"
                    {...register('department')}
                    disabled={loading}
                  />
                </div>

                <div className="space-y-2">
                  <Label htmlFor="position">Cargo</Label>
                  <Input
                    id="position"
                    {...register('position')}
                    disabled={loading}
                  />
                </div>
              </div>
            </div>

            {/* Captura Facial */}
            <div className="space-y-4">
              <h3 className="text-lg font-semibold">Reconhecimento Facial *</h3>
              <FaceCapture onCapture={setFaceImage} />
            </div>

            {/* Ações */}
            <div className="flex gap-4 justify-end pt-4">
              <Button
                type="button"
                variant="outline"
                onClick={() => router.push('/colaboradores')}
                disabled={loading}
              >
                Cancelar
              </Button>
              <Button type="submit" disabled={loading}>
                {loading ? 'Cadastrando...' : 'Cadastrar Colaborador'}
              </Button>
            </div>
          </form>
        </CardContent>
      </Card>
    </div>
  );
}
