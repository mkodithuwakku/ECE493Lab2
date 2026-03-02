import React, { useState } from "react";
import { saveMetadata } from "../services/metadata_client";

function splitList(value: string): string[] {
  return value
    .split(",")
    .map((item) => item.trim())
    .filter((item) => item.length > 0);
}

export function MetadataPage() {
  const [authorNames, setAuthorNames] = useState("");
  const [affiliations, setAffiliations] = useState("");
  const [contactEmail, setContactEmail] = useState("");
  const [abstract, setAbstract] = useState("");
  const [keywords, setKeywords] = useState("");
  const [paperSource, setPaperSource] = useState("");
  const [message, setMessage] = useState<string | null>(null);
  const [locked, setLocked] = useState(false);

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    setMessage(null);

    const response = await saveMetadata({
      author_names: splitList(authorNames),
      affiliations: splitList(affiliations),
      contact_email: contactEmail,
      abstract,
      keywords: splitList(keywords),
      paper_source: paperSource,
    });

    if (response.status === 409) {
      setLocked(true);
    }
    if (response.payload.message) {
      setMessage(response.payload.message as string);
      return;
    }

    setMessage("Metadata submission failed. Please retry.");
  };

  return (
    <section>
      <h2>Paper Metadata</h2>
      {message && <p>{message}</p>}
      <form onSubmit={handleSubmit}>
        <label>
          Author Names (comma separated)
          <input
            type="text"
            value={authorNames}
            onChange={(event) => setAuthorNames(event.target.value)}
            disabled={locked}
          />
        </label>
        <label>
          Affiliations (comma separated)
          <input
            type="text"
            value={affiliations}
            onChange={(event) => setAffiliations(event.target.value)}
            disabled={locked}
          />
        </label>
        <label>
          Contact Email
          <input
            type="email"
            value={contactEmail}
            onChange={(event) => setContactEmail(event.target.value)}
            disabled={locked}
          />
        </label>
        <label>
          Abstract
          <textarea
            value={abstract}
            onChange={(event) => setAbstract(event.target.value)}
            disabled={locked}
          />
        </label>
        <label>
          Keywords (comma separated)
          <input
            type="text"
            value={keywords}
            onChange={(event) => setKeywords(event.target.value)}
            disabled={locked}
          />
        </label>
        <label>
          Paper Source
          <input
            type="text"
            value={paperSource}
            onChange={(event) => setPaperSource(event.target.value)}
            disabled={locked}
          />
        </label>
        <button type="submit" disabled={locked}>
          Save Metadata
        </button>
      </form>
    </section>
  );
}
