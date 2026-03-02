import React, { FormEvent, useState } from "react";
import { registerUser } from "../services/registration_client";
import {
  RegistrationResponse,
  RegistrationSuccess,
  ValidationErrorResponse,
} from "../services/registration_types";

interface RegistrationFormProps {
  onSuccess: (redirectTo: string, message: string) => void;
  onError: (message: string) => void;
  onValidationErrors: (errors: string[]) => void;
}

export function RegistrationForm({
  onSuccess,
  onError,
  onValidationErrors,
}: RegistrationFormProps) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [submitting, setSubmitting] = useState(false);

  const handleSubmit = async (event: FormEvent) => {
    event.preventDefault();
    if (submitting) {
      return;
    }
    setSubmitting(true);

    try {
      const response = (await registerUser({ email, password })) as RegistrationResponse;
      if ("redirect_to" in response) {
        onSuccess(response.redirect_to, response.message);
        return;
      }
      if ("errors" in response) {
        onValidationErrors((response as ValidationErrorResponse).errors);
        return;
      }
      onError((response as { message: string }).message);
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <label>
        Email
        <input
          type="email"
          value={email}
          onChange={(event) => setEmail(event.target.value)}
          required
        />
      </label>
      <label>
        Password
        <input
          type="password"
          value={password}
          onChange={(event) => setPassword(event.target.value)}
          required
        />
      </label>
      <button type="submit" disabled={submitting}>
        {submitting ? "Registering..." : "Register"}
      </button>
    </form>
  );
}
