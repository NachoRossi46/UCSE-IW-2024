import axios from 'axios';
import { useAuthStore } from '../store/auth/auth.store';


const loginAPI = axios.create({
  baseURL: process.env.REACT_APP_API_URL,
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