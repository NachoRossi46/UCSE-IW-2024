import { StateCreator, create } from 'zustand';
import type { AuthStatus, User } from '../../interfaces';
import { AuthService, LoginResponse } from '../../services/auth.service';
import { devtools, persist } from 'zustand/middleware';

export interface AuthState {

  status: AuthStatus;
  token?: string;
  user?: User;

  loginUser: (email: string, password: string) => Promise<LoginResponse>;
  checkAuthStatus: () => Promise<void>;
  logout: () => void;
}

const storeApi: StateCreator<AuthState> = (set) => ({
  status: 'Pending',
  token: undefined,
  user: undefined,

  loginUser: async (email: string, password: string): Promise<LoginResponse> => {
    try {
      const resp = await AuthService.login(email, password);
      set({ status: 'Authorized', token: resp.token, user: {
        id: resp.user_id,
        email: resp.email
      } })
      return resp;
    } catch (error) {
      set({ status: 'Unauthorized', token: undefined, user: undefined })
      throw 'Unauthorized'
    }
  },
  checkAuthStatus: async () => {
    try {
      const { token, ...user } = await AuthService.checkStatus();
      set({ status: 'Authorized', token, user: {
        id: user.user_id,
        email: user.email
      } });
    } catch (error) {
      set({ status: 'Unauthorized', token: undefined, user: undefined });
    }
  },
  logout: () => {
    set({ status: 'Unauthorized', token: undefined, user: undefined });
  },
});

export const useAuthStore = create<AuthState>()(
  devtools(
    persist(
      storeApi,
      { name: 'auth-storage' }
    )
    )
  );