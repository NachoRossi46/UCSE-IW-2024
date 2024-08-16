import { JwtPayload } from 'jwt-decode';

export enum CrudOperation {
  CREATE,
  READ,
  UPDATE,
  DELETE
}

export interface APIResult<T> {
  data: T;
  status: number;
}

export interface GetItemsPayload<T> {
  items: T[];
  count?: number;
}

export interface APIError {
  status: number;
  error: string;
  message: string;
  path: string;
  timestamp: string;
}
export interface User {
  token: string;
  username: string;
  jwt: UserJwtPayload;
}

export type UserJwtPayload = JwtPayload & {
  email: string;
  authorities: string[];
  firstName: string;
  lastName: string;
  //   type: UserType;
};

export interface ChangePassword {
  contraseña: string;
  email: string;
}