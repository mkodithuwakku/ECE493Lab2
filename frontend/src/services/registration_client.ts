import {
  DUPLICATE_EMAIL_MESSAGE,
  PASSWORD_REQUIREMENTS_MESSAGE,
  STORAGE_FAILURE_MESSAGE,
} from "./registration_messages";
import {
  MessageResponse,
  RegistrationRequest,
  RegistrationResponse,
  RegistrationSuccess,
  ValidationErrorResponse,
} from "./registration_types";

async function safeJson(response: Response): Promise<unknown> {
  try {
    return await response.json();
  } catch {
    return null;
  }
}

export async function registerUser(
  request: RegistrationRequest
): Promise<RegistrationResponse> {
  const response = await fetch("/register", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(request),
  });

  const payload = (await safeJson(response)) as RegistrationResponse | null;

  if (response.status === 201 && payload && "redirect_to" in payload) {
    return payload as RegistrationSuccess;
  }

  if (response.status === 400 && payload && "errors" in payload) {
    return payload as ValidationErrorResponse;
  }

  if (response.status === 409) {
    return { message: payload?.message || DUPLICATE_EMAIL_MESSAGE } as MessageResponse;
  }

  if (response.status === 422) {
    return {
      message: payload?.message || PASSWORD_REQUIREMENTS_MESSAGE,
    } as MessageResponse;
  }

  if (response.status === 500) {
    return { message: payload?.message || STORAGE_FAILURE_MESSAGE } as MessageResponse;
  }

  return { message: STORAGE_FAILURE_MESSAGE } as MessageResponse;
}
