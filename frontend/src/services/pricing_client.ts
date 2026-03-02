import {
  NO_PRICING_MESSAGE,
  PARTIAL_PRICING_MESSAGE,
  RETRIEVAL_ERROR_MESSAGE,
} from "./pricing_messages";
import {
  MessageResponse,
  PartialPricingResponse,
  PricingPayload,
  PricingResponse,
} from "./pricing_types";

async function safeJson(response: Response): Promise<unknown> {
  try {
    return await response.json();
  } catch {
    return null;
  }
}

export async function fetchPricing(): Promise<PricingPayload | MessageResponse> {
  const response = await fetch("/pricing");

  if (response.ok) {
    const payload = (await safeJson(response)) as PricingPayload | null;
    if (payload && (payload as PricingResponse).status === "ok") {
      return payload as PricingResponse;
    }
    if (payload && (payload as PartialPricingResponse).status === "partial") {
      return payload as PartialPricingResponse;
    }
    return { message: RETRIEVAL_ERROR_MESSAGE };
  }

  const payload = (await safeJson(response)) as MessageResponse | null;
  if (payload?.message) {
    return payload;
  }

  if (response.status === 404) {
    return { message: NO_PRICING_MESSAGE };
  }

  if (response.status === 206) {
    return { message: PARTIAL_PRICING_MESSAGE };
  }

  return { message: RETRIEVAL_ERROR_MESSAGE };
}
