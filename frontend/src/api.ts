import type { ChatResponse, SummaryResponse } from "./types";

// Backend base URL. Override with VITE_API_BASE in a .env file if the API runs
// somewhere other than the local dev server.
const API_BASE = import.meta.env.VITE_API_BASE ?? "http://127.0.0.1:8000";

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

export async function summarizeFile(file: File): Promise<SummaryResponse> {
  const form = new FormData();
  form.append("file", file);

  const res = await fetch(`${API_BASE}/summarize`, {
    method: "POST",
    body: form,
  });

  if (!res.ok) throw new Error(await parseError(res));
  return res.json();
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
