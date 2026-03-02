export interface RegistrationRequest {
  email: string;
  password: string;
}

export interface RegistrationSuccess {
  message: string;
  redirect_to: string;
}

export interface ValidationErrorResponse {
  errors: string[];
}

export interface MessageResponse {
  message: string;
}

export type RegistrationResponse =
  | RegistrationSuccess
  | ValidationErrorResponse
  | MessageResponse;
