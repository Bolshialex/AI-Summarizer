export interface Segment {
  start: number;
  end: number;
  text: string;
}

export interface SummaryResponse {
  id: string | null;
  video_name: string;
  summary: string;
  segments: Segment[];
}

export interface ChatMatch {
  id: string;
  video_name: string;
  summary: string;
  source: string | null;
  created_at: string;
  similarity: number;
}

export interface ChatResponse {
  query: string;
  matches: ChatMatch[];
}
