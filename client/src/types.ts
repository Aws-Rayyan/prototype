export type Confidence = "well_supported" | "partial" | "insufficient";

export type Citation = {
  doc_id: string;
  doc_title: string;
  snippet: string;
  relevance: number;
};

export type AskResponse = {
  question_id: string;
  answer: string;
  confidence: Confidence;
  citations: Citation[];
  retrieved_below_threshold: boolean;
};

export type User = {
  id: string;
  name: string;
  role: string;
};

export type ActionItem = {
  id: string;
  question_id: string;
  created_by: string;
  action_type: string;
  title: string;
  body: string;
  status: string;
  reviewed_by: string | null;
  reviewed_at: string | null;
  created_at: string;
};

export type AuditEntry = {
  id: string;
  event_type: string;
  user_id: string;
  detail: Record<string, unknown>;
  created_at: string;
};
