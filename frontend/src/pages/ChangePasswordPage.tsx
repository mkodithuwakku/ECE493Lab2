import React, { useState } from "react";
import { changePassword } from "../services/password_client";

export function ChangePasswordPage() {
  const [currentPassword, setCurrentPassword] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [message, setMessage] = useState<string | null>(null);
  const [errors, setErrors] = useState<string[]>([]);

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    setMessage(null);
    setErrors([]);

    const response = await changePassword({
      current_password: currentPassword,
      new_password: newPassword,
      confirm_password: confirmPassword,
    });

    if (response.status === 200) {
      setMessage(response.payload.message);
      return;
    }

    if (response.payload.errors) {
      setErrors(response.payload.errors as string[]);
      return;
    }

    if (response.payload.message) {
      setMessage(response.payload.message as string);
      return;
    }

    setMessage("Password could not be updated. Please try again.");
  };

  return (
    <section>
      <h2>Change Password</h2>
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
          Current Password
          <input
            type="password"
            value={currentPassword}
            onChange={(event) => setCurrentPassword(event.target.value)}
          />
        </label>
        <label>
          New Password
          <input
            type="password"
            value={newPassword}
            onChange={(event) => setNewPassword(event.target.value)}
          />
        </label>
        <label>
          Confirm New Password
          <input
            type="password"
            value={confirmPassword}
            onChange={(event) => setConfirmPassword(event.target.value)}
          />
        </label>
        <button type="submit">Update Password</button>
      </form>
    </section>
  );
}
