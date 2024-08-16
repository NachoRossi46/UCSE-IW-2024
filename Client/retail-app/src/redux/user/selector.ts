export const getUserSelector = (state: any) => state.userReducer.userState.user;
export const getAuthenticatedSelector = (state: any) => state.userReducer.userState.authenticated;
export const getAuthenticatingSelector = (state: any) => state.userReducer.userState.authenticating;
export const getErrorSelector = (state: any) => state.userReducer.userState.error;
export const getUserIsSet = (state: any) => state.userReducer.userState.userIsSet;
