import { removeUser } from '@/src/auth/authHelper';
import { UserActions, UserActionType, UserState } from './types';

const initialState: UserState = {
  authenticated: false,
  authenticating: false,
  error: false,
  isUserSet: false,
  user: undefined,
  passwordChanged: false,
};

const userReducer = (state: UserState = initialState, action: UserActions) => {
  switch (action.type) {
    case UserActionType.loginRequestedAction:
      return {
        ...state,
        authenticating: true,
        error: false,
        isUserSet: false
      };
    case UserActionType.loginDoneAction:
      return {
        ...state,
        authenticating: false,
        passwordChanged: false,
        isUserSet: false
      };
    case UserActionType.loginErrorAction:
      // showError('Credenciales invalidas!', 'credenciales-invalidas-error-message');
      return {
        ...state,
        user: undefined,
        authenticated: false,
        authenticating: false,
        error: true
      };
    case UserActionType.logoutDoneAction:
      removeUser();

      return {
        ...state,
        user: undefined,
        authenticated: false,
        authenticating: false,
        error: false,
        isUserSet: false
      };
    case UserActionType.setUserAction:
      return {
        ...state,
        user: action.payload,
        passwordChanged: false,
        isUserSet: false
      };
    case UserActionType.changePasswordAction:
      return {
        ...state,
        passwordChanged: true,
        isUserSet: false
      };
    default:
      return state;
  }
};

export default userReducer;
