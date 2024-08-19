import { loginAPI } from '@/api/login.api';
import LoginAPI from '@/api/LoginAPI';
import { AxiosError } from 'axios';

export interface LoginResponse {
  user_id: number;
  email: string;
  // fullName: string;
  // isActive: boolean;
  // roles: string[];
  token: string;
}

export class AuthService {
  // static login = async (email: string, password: string): Promise<LoginResponse> => {
  //   try {
  //     const { data } = await LoginAPI.login<LoginResponse>('/auth/login', {
  //       email,
  //       password,
  //     });
  //     return data;
  //   } catch (error) {
  //     if (error instanceof AxiosError) {
  //       console.log(error.response?.data);
  //       throw new Error();
  //     }
  //     throw new Error('Unable to login');
  //   }
  // }

  static login = async (email: string, password: string): Promise<LoginResponse> => {
    try {
      const response = await fetch('http://localhost:8000/auth/login/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          email,
          password,
        }),
      });
      
      if (!response.ok) {
        throw new Error('Unable to login');
      }

      const data: LoginResponse = await response.json();
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

