import type { AuthStatus, UserZ } from '@/src/interfaces';
import { AuthService } from '../../services/auth.service';
import { StateCreator, create } from 'zustand';
import { devtools, persist } from 'zustand/middleware';

export interface AuthState {
  status: AuthStatus;
  token?: string;
  user?: UserZ;

  loginUser: (email: string, password: string) => Promise<void>;
  checkAuthStatus: () => Promise<void>;
  logout: () => void;
}

const storeApi: StateCreator<AuthState> = (set) => ({
  status: 'Unauthorized',
  token: undefined,
  user: undefined,

  loginUser: async (email: string, password: string) => {
    try {
      const { token, ...user } = await AuthService.login(email, password);
      set({ status: 'Authorized', token, user });
    } catch (error) {
      set({ status: 'Unauthorized', token: undefined, user: undefined });
      throw 'Unauthorized';
    }
  },
  checkAuthStatus: async () => {
    try {
      const { token, ...user } = await AuthService.checkStatus();
      set({ status: 'Authorized', token, user });
    } catch (error) {
      set({ status: 'Unauthorized', token: undefined, user: undefined });
      throw new Error('Unauthorized'); //TODO Toastfy aca
    }
  },
  logout: () => {
    set({ status: 'Unauthorized', token: undefined, user: undefined });
  }
});

export const useAuthStore = create<AuthState>()(
  devtools(persist(storeApi, { name: 'auth-storage' }))
);
