import jwtDecode from 'jwt-decode';
import { HttpStatusCode } from 'axios';
// import { showError } from '../components/snackbars/AppSnackbar';
import { APIError, User, UserJwtPayload } from '../types/types';

const USER_LOCAL_KEY = 'sorteos_key';

export const setUser = (user: User) => {
  user.jwt = jwtDecode<UserJwtPayload>(user.token);
  localStorage.setItem(USER_LOCAL_KEY, JSON.stringify(user));
};

export const removeUser = () => {
  localStorage.removeItem(USER_LOCAL_KEY);
};

// export const getCurrentUser = () => {
//   var jwt = localStorage.getItem(USER_LOCAL_KEY);
//   if (jwt !== null) return JSON.parse(jwt);
//   else return null;
// };

// export const expiredToken = (): boolean => {
//   var user = getCurrentUser();
//   if (user === null) return true;

//   if (user.jwt === undefined) return true;

//   const expiration = new Date(user.jwt.exp * 1000);
//   if (expiration.getTime() < new Date().getTime()) return true;

//   return false;
// };

export const resolveLoginError = (error: APIError) => {
  console.log(error);

  // if (error === undefined) showError('Error al realizar la autenticación.', 'autenticacion-error-undefined');
  // else if (error.status === HttpStatusCode.Unauthorized)
  //   showError('Error al realizar la autenticación.', 'auth-error-no-autorizado');
  // else if (error.status === HttpStatusCode.InternalServerError)
  //   showError('Error al realizar la autenticación', 'auth-error-500');
};

// export const isAdmin = (user: User | undefined): boolean => {
//   if (user === undefined) return false;
//   return user.jwt.type === UserType.ADMIN;
// };
