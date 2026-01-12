'use client';

import { useRouter } from 'next/navigation';
import { Button } from '@/components/ui/button';
import { useAuthStore } from '@/store/authStore';
import { LogOut } from 'lucide-react';

export function Header() {
  const router = useRouter();
  const setToken = useAuthStore((state) => state.setToken);

  const handleLogout = () => {
    setToken(null);
    router.push('/login');
  };

  return (
    <header className="bg-white border-b px-8 py-4 flex justify-between items-center">
      <h1 className="text-2xl font-bold">Sistema de Reconhecimento Facial</h1>
      <Button variant="outline" onClick={handleLogout}>
        <LogOut className="mr-2 h-4 w-4" />
        Sair
      </Button>
    </header>
  );
}

