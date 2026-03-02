import React, { useState } from "react";
import { saveDraft } from "../services/draft_client";

function splitAuthors(value: string): string[] {
  return value
    .split(",")
    .map((item) => item.trim())
    .filter((item) => item.length > 0);
}

export function SubmissionProgressPage() {
  const [title, setTitle] = useState("");
  const [abstract, setAbstract] = useState("");
  const [authors, setAuthors] = useState("");
  const [contactEmail, setContactEmail] = useState("");
  const [message, setMessage] = useState<string | null>(null);
  const [warning, setWarning] = useState<string | null>(null);
  const [pendingPayload, setPendingPayload] = useState<Record<string, unknown> | null>(
    null,
  );

  const buildPayload = () => ({
    title,
    abstract,
    authors: splitAuthors(authors),
    contact_email: contactEmail,
  });

  const handleSave = async (saveAnyway: boolean) => {
    const data = pendingPayload ?? buildPayload();
    setMessage(null);
    setWarning(null);

    const response = await saveDraft({ data, save_anyway: saveAnyway });

    if (response.status === 409) {
      setWarning(response.payload.message as string);
      setPendingPayload(data);
      return;
    }

    if (response.payload.message) {
      setMessage(response.payload.message as string);
      setPendingPayload(null);
      return;
    }

    setMessage("Draft save failed. Please retry.");
    setPendingPayload(null);
  };

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    await handleSave(false);
  };

  return (
    <section>
      <h2>Save Submission Progress</h2>
      {message && <p>{message}</p>}
      {warning && (
        <div>
          <p>{warning}</p>
          <button type="button" onClick={() => handleSave(true)}>
            Save Anyway
          </button>
          <button type="button" onClick={() => setWarning(null)}>
            Cancel
          </button>
        </div>
      )}
      <form onSubmit={handleSubmit}>
        <label>
          Title
          <input
            type="text"
            value={title}
            onChange={(event) => setTitle(event.target.value)}
          />
        </label>
        <label>
          Abstract
          <textarea
            value={abstract}
            onChange={(event) => setAbstract(event.target.value)}
          />
        </label>
        <label>
          Authors (comma separated)
          <input
            type="text"
            value={authors}
            onChange={(event) => setAuthors(event.target.value)}
          />
        </label>
        <label>
          Contact Email
          <input
            type="email"
            value={contactEmail}
            onChange={(event) => setContactEmail(event.target.value)}
          />
        </label>
        <button type="submit">Save Draft</button>
      </form>
    </section>
  );
}
