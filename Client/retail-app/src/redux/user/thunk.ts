import { AppThunk } from '../store';
import { LoginAPI } from "../../api/LoginAPI";
import { logInDone, logInError, logInRequest } from './slice';

export const thunkLogIn = (username: string, password: string): AppThunk => {
  return async (dispatch) => {
    dispatch(logInRequest());

    try {
      const response = await LoginAPI.login(username, password);

      dispatch(logInDone(response.data));
    } catch (err) {
      // showError('ERROR', 'login-error'); //TODO Crear toastify aca
      dispatch(logInError());
    }
  };
};
