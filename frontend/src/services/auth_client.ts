import { LoginResponse } from "./auth_types";

export async function loginUser(
  identifier: string,
  password: string
): Promise<LoginResponse> {
  const response = await fetch("/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ identifier, password }),
  });

  const payload = await response.json();
  return payload as LoginResponse;
}
