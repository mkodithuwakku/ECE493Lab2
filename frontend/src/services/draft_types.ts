export interface DraftSaveRequest {
  data: Record<string, unknown>;
  save_anyway?: boolean;
}

export interface DraftSaveResponse {
  message: string;
  status?: "complete" | "incomplete";
}
