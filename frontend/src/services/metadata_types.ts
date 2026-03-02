export interface MetadataRequest {
  author_names: string[];
  affiliations: string[];
  contact_email: string;
  abstract: string;
  keywords: string[];
  paper_source: string;
}

export interface MessageResponse {
  message: string;
}
