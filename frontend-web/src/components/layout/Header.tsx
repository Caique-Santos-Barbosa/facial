'use client';

import { useRouter } from 'next/navigation';
import { useAuthStore } from '@/store/authStore';
import { Button } from '@/components/ui/button';
import { LogOut } from 'lucide-react';

export function Header() {
  const router = useRouter();
  const { user, clearAuth } = useAuthStore();

  const handleLogout = () => {
    clearAuth();
    router.push('/login');
  };

  return (
    <header className="h-16 border-b border-slate-200 bg-white px-8 flex items-center justify-between">
      <div>
        <h2 className="text-xl font-semibold text-slate-900">
          Sistema de Reconhecimento Facial
        </h2>
      </div>
      
      <div className="flex items-center gap-4">
        <div className="text-sm">
          <p className="font-medium text-slate-900">{user?.full_name}</p>
          <p className="text-slate-500">{user?.email}</p>
        </div>
        
        <Button variant="outline" onClick={handleLogout}>
          <LogOut className="h-4 w-4 mr-2" />
          Sair
        </Button>
      </div>
    </header>
  );
}
