import React, { useState } from "react";
import { RegistrationForm } from "../components/registration_form";

export function RegisterPage() {
  const [message, setMessage] = useState<string | null>(null);
  const [errors, setErrors] = useState<string[]>([]);

  const handleSuccess = (redirectTo: string, successMessage: string) => {
    setErrors([]);
    setMessage(successMessage);
    window.location.assign(redirectTo);
  };

  const handleError = (errorMessage: string) => {
    setErrors([]);
    setMessage(errorMessage);
  };

  const handleValidationErrors = (validationErrors: string[]) => {
    setMessage(null);
    setErrors(validationErrors);
  };

  return (
    <section>
      <h2>Create an Account</h2>
      {message && <p>{message}</p>}
      {errors.length > 0 && (
        <ul>
          {errors.map((error) => (
            <li key={error}>{error}</li>
          ))}
        </ul>
      )}
      <RegistrationForm
        onSuccess={handleSuccess}
        onError={handleError}
        onValidationErrors={handleValidationErrors}
      />
    </section>
  );
}
