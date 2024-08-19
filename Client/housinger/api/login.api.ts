import { useAuthStore } from '@/store/auth/auth.store';
import axios from 'axios';

const loginAPI = axios.create({
  baseURL: process.env.REACT_APP_API_URL,
  // baseURL: 'http://localhost:3000/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

loginAPI.interceptors.request.use(
  (config) => {
    const token = useAuthStore.getState().token;
    // console.log({token});

    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }

    return config;
  })

export {
  loginAPI,
}