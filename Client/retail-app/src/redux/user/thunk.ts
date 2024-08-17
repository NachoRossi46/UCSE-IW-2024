import { AppThunk } from '../store';
import LoginAPI from '@/src/api/LoginAPI';
import { getCurrentUser } from '@/src/auth/authHelper';
import { ChangePassword } from '@/src/types/types';
import Toastify from 'toastify-js';
import { loginDoneAction, loginRequestedAction, changePasswodAction, loginErrorAction, logoutDoneAction } from './action';

export const thunkLogIn = (username: string, password: string): AppThunk => {
  return async (dispatch) => {
    dispatch(loginRequestedAction());
    try {
      // const user = await LoginAPI.login(username, password);

      dispatch(loginDoneAction());
    } catch (err) {
      // showError('ERROR', 'login-error'); //TODO Crear toastify aca
      dispatch(loginErrorAction());
    }
  };
};

export const thunkLogout = (): AppThunk => async (dispatch) => {
  try {
    const user = getCurrentUser();

    if (user) {
      await LoginAPI.logout();
      dispatch(logoutDoneAction(user));
    }
  } catch {
    dispatch(loginErrorAction());
  }
};

export const thunkChangePassword =
  (data: ChangePassword): AppThunk =>
  async (dispatch) => {
    try {
      await LoginAPI.changePassword(data);
      dispatch(changePasswodAction(data));
    } catch {
      Toastify({
        text: "Ocurrió un error al iniciar sesión.",
        duration: 3000,
        close: true,
        gravity: "bottom", // `top` or `bottom`
        position: 'left', // `left`, `center` or `right`
        backgroundColor: "linear-gradient(to right, #FF4848, #FF6E48)",
      }).showToast(); //Puede que falte importar el css de toastify
    }
  };
