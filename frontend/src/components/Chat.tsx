import { useState } from "react";
import { searchSummaries } from "../api";
import type { ChatMatch } from "../types";

export default function Chat() {
  const [query, setQuery] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [matches, setMatches] = useState<ChatMatch[] | null>(null);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    const q = query.trim();
    if (!q) return;

    setLoading(true);
    setError(null);
    setMatches(null);
    try {
      const res = await searchSummaries(q);
      setMatches(res.matches);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Something went wrong");
    } finally {
      setLoading(false);
    }
  }

  return (
    <section className="section">
      <div className="section-head">
        <span className="eyebrow">Search</span>
        <h2>Search your summaries</h2>
      </div>

      <form className="card search" onSubmit={handleSubmit}>
        <input
          type="text"
          value={query}
          placeholder="Ask about anything you've summarized…"
          onChange={(e) => setQuery(e.target.value)}
          disabled={loading}
        />
        <button type="submit" disabled={!query.trim() || loading}>
          {loading ? "Searching…" : "Search"}
        </button>
      </form>

      {error && <p className="error">{error}</p>}

      {matches && matches.length === 0 && (
        <p className="hint">No matching summaries found.</p>
      )}

      {matches && matches.length > 0 && (
        <ul className="matches">
          {matches.map((m) => (
            <li key={m.id} className="card match">
              <div className="match-head">
                <h3>{m.video_name}</h3>
                <span className="score">
                  {(m.similarity * 100).toFixed(0)}% match
                </span>
              </div>
              <p className="summary-text">{m.summary}</p>
            </li>
          ))}
        </ul>
      )}
    </section>
  );
}
