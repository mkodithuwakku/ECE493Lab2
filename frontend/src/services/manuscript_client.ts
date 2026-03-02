export interface ManuscriptUploadRequest {
  filename: string;
  size_bytes: number;
}

export async function uploadManuscript(request: ManuscriptUploadRequest) {
  const response = await fetch("/submissions/current/manuscript", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(request),
  });

  const payload = await response.json();
  return { status: response.status, payload };
}
