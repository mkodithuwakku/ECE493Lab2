export type PricingStatus = "ok" | "partial";

export interface PriceItem {
  attendance_type: string;
  amount: number;
}

export interface PricingResponse {
  status: "ok";
  prices: PriceItem[];
}

export interface PartialPricingResponse {
  status: "partial";
  prices: PriceItem[];
  warning: string;
}

export interface MessageResponse {
  message: string;
}

export type PricingPayload = PricingResponse | PartialPricingResponse;
