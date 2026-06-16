import type { ChatResponse, SummaryResponse } from "./types";

// Backend base URL. Override with VITE_API_BASE in a .env file if the API runs
// somewhere other than the local dev server.
const API_BASE = (
  import.meta.env.VITE_API_BASE ?? "http://127.0.0.1:8000"
).replace(/\/+$/, "");

async function parseError(res: Response): Promise<string> {
  try {
    const data = await res.json();
    if (typeof data?.detail === "string") return data.detail;
    if (data?.detail) return JSON.stringify(data.detail);
    return `${res.status} ${res.statusText}`;
  } catch {
    return `${res.status} ${res.statusText}`;
  }
}

export interface SummarizeProgress {
  stage: "transcribing" | "summarizing" | "embedding" | "saving";
  message?: string;
  done?: number;
  total?: number;
}

// The backend streams Server-Sent Events: `progress`/`stage` updates followed
// by a single `result` (or `error`). We read the stream and forward progress
// to the caller, resolving with the final summary.
export async function summarizeFile(
  file: File,
  onProgress?: (p: SummarizeProgress) => void,
): Promise<SummaryResponse> {
  const form = new FormData();
  form.append("file", file);

  const res = await fetch(`${API_BASE}/summarize`, {
    method: "POST",
    body: form,
  });

  if (!res.ok || !res.body) throw new Error(await parseError(res));

  const reader = res.body.getReader();
  const decoder = new TextDecoder();
  let buffer = "";
  let result: SummaryResponse | null = null;

  for (;;) {
    const { done, value } = await reader.read();
    if (done) break;

    buffer += decoder.decode(value, { stream: true });
    const frames = buffer.split("\n\n");
    buffer = frames.pop() ?? "";

    for (const frame of frames) {
      const line = frame.trim();
      if (!line.startsWith("data:")) continue;

      const msg = JSON.parse(line.slice(5).trim());
      if (msg.event === "result") {
        result = {
          id: msg.id,
          video_name: msg.video_name,
          summary: msg.summary,
          segments: msg.segments,
        };
      } else if (msg.event === "error") {
        throw new Error(msg.message ?? "Something went wrong");
      } else {
        onProgress?.(msg as SummarizeProgress);
      }
    }
  }

  if (!result) throw new Error("The server finished without returning a summary");
  return result;
}

export async function searchSummaries(
  query: string,
  matchCount = 5,
): Promise<ChatResponse> {
  const res = await fetch(`${API_BASE}/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ query, match_count: matchCount }),
  });

  if (!res.ok) throw new Error(await parseError(res));
  return res.json();
}
