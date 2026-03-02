import { MetadataRequest } from "./metadata_types";

export async function saveMetadata(request: MetadataRequest) {
  const response = await fetch("/submissions/current/metadata", {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(request),
  });

  const payload = await response.json();
  return { status: response.status, payload };
}
