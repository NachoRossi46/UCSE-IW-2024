import { AxiosError } from "axios";
import { loginAPI } from "../api/login.api";

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
      const response = await loginAPI.post<LoginResponse>('/login', { email, password });

      return response.data;
    } catch (error) {
      if (error instanceof AxiosError) {
        console.log(error.response?.data);
        throw new Error(error.response?.data?.message || 'An error occurred');        
      }
      throw new Error('Unable to login');
    }
  };

  static checkStatus = async (): Promise<LoginResponse> => {
    try {
      const {data} = await loginAPI.get<LoginResponse>('/auth/status');
      return data;
    } catch (error) {
      throw new Error('Unable to check status/Unauthorized');
    }
  }

}

