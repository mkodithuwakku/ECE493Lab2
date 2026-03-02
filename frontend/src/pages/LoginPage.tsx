import React, { useState } from "react";
import { loginUser } from "../services/auth_client";
import {
  AccountStatusError,
  InvalidCredentials,
  LoginResponse,
  LoginSuccess,
  MessageResponse,
  ValidationError,
} from "../services/auth_types";

export function LoginPage() {
  const [identifier, setIdentifier] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState<string | null>(null);
  const [errors, setErrors] = useState<string[]>([]);

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    setMessage(null);
    setErrors([]);

    const response = (await loginUser(identifier, password)) as LoginResponse;

    if ((response as LoginSuccess).redirect_to) {
      const success = response as LoginSuccess;
      setMessage(success.message);
      window.location.assign(success.redirect_to);
      return;
    }

    if ((response as ValidationError).errors) {
      setErrors((response as ValidationError).errors);
      return;
    }

    if ((response as InvalidCredentials).remaining_attempts !== undefined) {
      const invalid = response as InvalidCredentials;
      setMessage(
        `${invalid.message} Remaining attempts: ${invalid.remaining_attempts}.`
      );
      return;
    }

    if ((response as AccountStatusError).status) {
      const status = response as AccountStatusError;
      setMessage(status.message);
      return;
    }

    const fallback = response as MessageResponse;
    setMessage(fallback.message);
  };

  return (
    <section>
      <h2>Log In</h2>
      {message && <p>{message}</p>}
      {errors.length > 0 && (
        <ul>
          {errors.map((error) => (
            <li key={error}>{error}</li>
          ))}
        </ul>
      )}
      <form onSubmit={handleSubmit}>
        <label>
          Username or Email
          <input
            type="text"
            value={identifier}
            onChange={(event) => setIdentifier(event.target.value)}
          />
        </label>
        <label>
          Password
          <input
            type="password"
            value={password}
            onChange={(event) => setPassword(event.target.value)}
          />
        </label>
        <button type="submit">Log In</button>
      </form>
    </section>
  );
}
