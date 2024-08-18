import { loginAPI } from '@/api/login.api';
import { AxiosError } from 'axios';


export interface LoginResponse {
  id: string;
  email: string;
  fullName: string;
  isActive: boolean;
  roles: string[];
  token: string;
}

export class AuthService {
  static login = async (email: string, password: string): Promise<LoginResponse> => {
    try {
      const { data } = await loginAPI.post<LoginResponse>('/auth/login', {
        email,
        password,
      });
      return data;
    } catch (error) {
      if (error instanceof AxiosError) {
        console.log(error.response?.data);
        throw new Error();
      }

      throw new Error('Unable to login');
    }
  }

  static checkStatus = async (): Promise<LoginResponse> => {
    try {
      const {data} = await loginAPI.get<LoginResponse>('/auth/status');
      return data;
    } catch (error) {
      throw new Error('Unable to check status/Unauthorized');
    }
  }

  // static logout = async (): Promise<void> => {
  //   try {
  //     await tesloApi.post('/auth/logout');
  //   } catch (error) {
  //     throw new Error('Unable to logout');
  //   }
  // }

}

