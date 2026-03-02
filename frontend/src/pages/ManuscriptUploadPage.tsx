import React, { useState } from "react";
import { uploadManuscript } from "../services/manuscript_client";

export function ManuscriptUploadPage() {
  const [filename, setFilename] = useState("");
  const [sizeBytes, setSizeBytes] = useState(0);
  const [message, setMessage] = useState<string | null>(null);

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    setMessage(null);

    const response = await uploadManuscript({ filename, size_bytes: sizeBytes });
    if (response.payload.message) {
      setMessage(response.payload.message as string);
      return;
    }
    setMessage("Upload failed. Please retry.");
  };

  return (
    <section>
      <h2>Upload Manuscript</h2>
      {message && <p>{message}</p>}
      <form onSubmit={handleSubmit}>
        <label>
          Filename
          <input
            type="text"
            value={filename}
            onChange={(event) => setFilename(event.target.value)}
          />
        </label>
        <label>
          File Size (bytes)
          <input
            type="number"
            value={sizeBytes}
            onChange={(event) => setSizeBytes(Number(event.target.value))}
          />
        </label>
        <button type="submit">Upload</button>
      </form>
    </section>
  );
}
