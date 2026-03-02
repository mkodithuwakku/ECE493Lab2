export interface LoginSuccess {
  message: string;
  redirect_to: string;
}

export interface ValidationError {
  errors: string[];
}

export interface InvalidCredentials {
  message: string;
  remaining_attempts: number;
}

export interface AccountStatusError {
  message: string;
  status: "locked" | "disabled";
}

export interface MessageResponse {
  message: string;
}

export type LoginResponse =
  | LoginSuccess
  | ValidationError
  | InvalidCredentials
  | AccountStatusError
  | MessageResponse;
