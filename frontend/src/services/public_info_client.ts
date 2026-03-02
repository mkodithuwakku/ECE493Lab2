import {
  PARTIAL_CONTENT_MESSAGE,
  RETRIEVAL_ERROR_MESSAGE,
  WEBSITE_UNAVAILABLE_MESSAGE,
} from "./public_info_messages";
import {
  ErrorResponse,
  PartialPublicInfoResponse,
  PublicInfoPayload,
  PublicInfoResponse,
} from "./public_info_types";

async function safeJson(response: Response): Promise<unknown> {
  try {
    return await response.json();
  } catch {
    return null;
  }
}

export async function fetchPublicInfo(): Promise<PublicInfoPayload | ErrorResponse> {
  const response = await fetch("/");

  if (response.ok) {
    const payload = (await safeJson(response)) as PublicInfoPayload | null;
    if (payload && (payload as PublicInfoResponse).status === "ok") {
      return payload as PublicInfoResponse;
    }
    if (payload && (payload as PartialPublicInfoResponse).status === "partial") {
      return payload as PartialPublicInfoResponse;
    }
    return { message: RETRIEVAL_ERROR_MESSAGE };
  }

  const payload = (await safeJson(response)) as ErrorResponse | null;
  if (payload?.message) {
    return payload;
  }

  if (response.status === 503) {
    return { message: WEBSITE_UNAVAILABLE_MESSAGE };
  }

  if (response.status === 206) {
    return { message: PARTIAL_CONTENT_MESSAGE };
  }

  return { message: RETRIEVAL_ERROR_MESSAGE };
}
