import { DraftSaveRequest } from "./draft_types";

export async function saveDraft(request: DraftSaveRequest) {
  const response = await fetch("/submissions/current/draft", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(request),
  });

  const payload = await response.json();
  return { status: response.status, payload };
}
