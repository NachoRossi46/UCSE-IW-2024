import { PayloadAction, createSlice } from '@reduxjs/toolkit';
import { User } from '../../types/types';
import { removeUser, setUser } from '@/src/auth/authHelper';
// import { showError, showMessage } from '../../components/snackbars/AppSnackbar';
import "toastify-js/src/toastify.css";
import Toastify from 'toastify-js';

type InitialState = {
  userState: UserState;
};

export type UserState = {
  authenticated: boolean;
  authenticating: boolean;
  userIsSet: boolean;
  error: boolean;
  user?: User;
};

const initialState = {
  userState: {
    authenticated: false,
    authenticating: false,
    error: false,
    user: undefined,
    userIsSet: false
  } as UserState
} as InitialState;

export const user = createSlice({
  name: 'user',
  initialState,
  reducers: {
    logOut: () => {
      removeUser();
      return { userState: { ...initialState.userState, userIsSet: true } };
    },
    logInRequest: (state) => {
      return {
        userState: {
          ...state.userState,
          authenticating: true,
          error: false,
          userIsSet: false
        }
      };
    },
    logInDone: (state, action: PayloadAction<User>) => {
      setUser(action.payload);
      return {
        userState: {
          user: action.payload,
          authenticated: true,
          error: false,
          authenticating: false,
          userIsSet: true
        }
      };
    },
    logInError: (state) => {
      // showError('Ocurrió un error al iniciar sesión.', 'error-inicio-sesion');
      Toastify({
        text: "Ocurrió un error al iniciar sesión.",
        duration: 3000,
        close: true,
        gravity: "top", // `top` or `bottom`
        position: 'right', // `left`, `center` or `right`
        backgroundColor: "linear-gradient(to right, #FF4848, #FF6E48)",
      }).showToast();
      return {
        userState: {
          ...state.userState,
          error: true,
          loading: false,
          userIsSet: false
        }
      };
    },
    setUserAction: (state, action: PayloadAction<User>) => {
      return {
        userState: {
          user: action.payload,
          authenticated: !!action.payload,
          authenticating: false,
          error: false,
          userIsSet: true
        }
      };
    }
  }
});

export const { logOut, logInRequest, logInDone, logInError, setUserAction } = user.actions;
export default user.reducer;

