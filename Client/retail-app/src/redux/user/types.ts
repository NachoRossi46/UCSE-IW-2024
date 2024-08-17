import { Action } from 'redux';
import { ChangePassword, User } from '../../types/types';
import { ActionPayload } from '../action';

export interface UserState {
  authenticated: boolean;
  authenticating: boolean;
  error: boolean;
  isUserSet: boolean;
  user?: User;
  passwordChanged: boolean;
}

export enum UserActionType {
  isAuthenticatedAction = 'user/is-authenticated-user',
  getCurrentUserAction = 'user/get-current-user',
  loginDoneAction = 'user/login-done',
  loginErrorAction = 'user/login-error',
  logoutDoneAction = 'user/logout-done',
  loginRequestedAction = 'user/requested-done',
  setUserAction = 'user/set-user',
  changePasswordAction = 'user/change-password',
}
/*
export interface IsAuthenticatedAction
  extends Action<UserActionType.isAuthenticatedAction> {}
*/
export interface LoginRequestedAction extends Action<UserActionType.loginRequestedAction> {}

export interface LoginDoneAction
  extends ActionPayload<UserActionType.loginDoneAction, User> {}
export interface LoginErrorAction extends Action<UserActionType.loginErrorAction> {}

export interface LogoutDoneAction extends ActionPayload<UserActionType.logoutDoneAction, User> {}

export interface SetUserAction extends ActionPayload<UserActionType.setUserAction, User> {}

export interface ChangePasswordAction
  extends ActionPayload<UserActionType.changePasswordAction, ChangePassword> {}

export type UserActions =
  | LoginDoneAction
  | LoginErrorAction
  | LogoutDoneAction
  | LoginRequestedAction
  | SetUserAction
  | ChangePasswordAction;
