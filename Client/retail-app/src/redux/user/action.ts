import { ChangePassword, User } from '../../types/types';
import {
  ChangePasswordAction,
  LoginDoneAction,
  LoginErrorAction,
  LoginRequestedAction,
  LogoutDoneAction,
  SetUserAction,
  UserActionType,
} from './types';

/*
export const isAuthenticatedAction = (): IsAuthenticatedAction => {
  return { type: UserActionType.isAuthenticatedAction };
};
*/
export const loginRequestedAction = (): LoginRequestedAction => {
  return { type: UserActionType.loginRequestedAction };
};

export const loginDoneAction = (): LoginDoneAction => {
  return { type: UserActionType.loginDoneAction };
};

export const loginErrorAction = (): LoginErrorAction => {
  return { type: UserActionType.loginErrorAction };
};

export const logoutDoneAction = (user: User): LogoutDoneAction => {
  return { type: UserActionType.logoutDoneAction, payload: user };
};

export const setUserAction = (user: User): SetUserAction => {
  return { type: UserActionType.setUserAction, payload: user };
};

export const changePasswodAction = (data: ChangePassword): ChangePasswordAction => {
  return { type: UserActionType.changePasswordAction, payload: data };
};
