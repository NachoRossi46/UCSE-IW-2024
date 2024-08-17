import { Action } from 'redux';

export interface ActionPayload<TAction, TPayload> extends Action<TAction> {
  payload: TPayload;
}
