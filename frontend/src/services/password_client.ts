export interface ChangePasswordRequest {
  current_password: string;
  new_password: string;
  confirm_password: string;
}

export async function changePassword(request: ChangePasswordRequest) {
  const response = await fetch("/account/password", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(request),
  });

  const payload = await response.json();
  return { status: response.status, payload };
}
