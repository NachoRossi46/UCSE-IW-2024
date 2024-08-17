import { UserState } from "./slice";

interface State {
  user: UserState;
}

export const userSelector = (state: State) => state.user.user;
// export const getUserSelector = (state: any) => state.userReducer.userState.user;
export const isAuthenticatorSelector = (state: State) => state.user.authenticated;
// export const getAuthenticatedSelector = (state: any) => state.userReducer.userState.authenticated;
export const isAuthenticatingSelector = (state: State) => state.user.authenticating;
// export const getAuthenticatingSelector = (state: any) => state.userReducer.userState.authenticating;
export const loginErrorUserSelector = (state: State) => state.user.error;
// export const getErrorSelector = (state: any) => state.userReducer.userState.error;
export const isUserSetSelector = (state: State) => state.user.isUserSet;
// export const getUserIsSet = (state: any) => state.userReducer.userState.userIsSet;

export const passwordChangedSelector = (state: State) => state.user.passwordChanged;

