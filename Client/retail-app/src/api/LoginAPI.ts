import axios from 'axios';
import { APIResult, ChangePassword, User } from '../types/types';
// import { getCurrentUser } from '../auth/authHelper';

class LoginAPI {
  http() {
    const headers = {
      'Content-type': 'application/json'
    };

    return axios.create({
      baseURL: process.env.REACT_APP_API_ENDPOINT,
      headers: headers
    });
  }

  httpSecure() {
    // const user = getCurrentUser();

    const headers = {
      'Content-type': 'application/json',
      // Authorization: user.token
    };

    return axios.create({
      baseURL: process.env.REACT_APP_API_ENDPOINT,
      headers: headers
    });
  }

  async login(username: string, password: string): Promise<APIResult<User>> {
    return this.http().post<User>('/security/login', {
      username: username,
      password: password
    });
  }

  async logout(): Promise<void> {
    return this.httpSecure().post('/security/logout');
  }

  async changePassword(data: ChangePassword): Promise<APIResult<void>> {
    // const user = getCurrentUser();
    return this.httpSecure().post(
      `/security/change-password`,
      {
        contraseña: data.contraseña,
        email: data.email
      },
      {
        headers: {
          // Authorization: user.token,
          'Content-Type': 'application/json'
        }
      }
    );
  }
}

export default new LoginAPI();
