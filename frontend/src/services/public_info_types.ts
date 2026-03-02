export type PublicInfoStatus = "ok" | "partial";

export interface PublicItem {
  content: string;
}

export interface PublicInfoResponse {
  status: "ok";
  announcements: PublicItem[];
  information: PublicItem[];
  message?: string;
}

export interface PartialPublicInfoResponse {
  status: "partial";
  announcements: PublicItem[];
  information: PublicItem[];
  warning: string;
}

export interface ErrorResponse {
  message: string;
}

export type PublicInfoPayload = PublicInfoResponse | PartialPublicInfoResponse;
