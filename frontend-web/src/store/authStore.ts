import { create } from 'zustand';
import { persist } from 'zustand/middleware';

interface User {
  id: number;
  username: string;
  email: string;
  full_name: string;
  is_superuser: boolean;
}

interface AuthState {
  user: User | null;
  token: string | null;
  setAuth: (user: User, token: string) => void;
  clearAuth: () => void;
  isAuthenticated: () => boolean;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set, get) => ({
      user: null,
      token: null,
      
      setAuth: (user, token) => {
        localStorage.setItem('access_token', token);
        set({ user, token });
      },
      
      clearAuth: () => {
        localStorage.removeItem('access_token');
        set({ user: null, token: null });
      },
      
      isAuthenticated: () => {
        return !!get().token;
      },
    }),
    {
      name: 'auth-storage',
    }
  )
);
