import { useState } from "react";
import { searchSummaries } from "../api";
import { formatDate } from "../format";
import type { ChatMatch } from "../types";

const MATCH_COUNTS = [3, 5, 10];
const CLAMP_LENGTH = 280;

function MatchCard({ match }: { match: ChatMatch }) {
  const [expanded, setExpanded] = useState(false);
  const long = match.summary.length > CLAMP_LENGTH;

  return (
    <li className="card match">
      <div className="match-head">
        <h3>{match.video_name}</h3>
        <span className="score">{(match.similarity * 100).toFixed(0)}% match</span>
      </div>

      <p className={`summary-text${long && !expanded ? " clamp" : ""}`}>
        {match.summary}
      </p>

      {long && (
        <button
          type="button"
          className="link"
          onClick={() => setExpanded((v) => !v)}
        >
          {expanded ? "Show less" : "Show more"}
        </button>
      )}

      {(match.source || match.created_at) && (
        <div className="match-meta">
          {match.source && <span>{match.source}</span>}
          {match.created_at && <span>{formatDate(match.created_at)}</span>}
        </div>
      )}
    </li>
  );
}

export default function Chat() {
  const [query, setQuery] = useState("");
  const [matchCount, setMatchCount] = useState(5);
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
      const res = await searchSummaries(q, matchCount);
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
        <label className="match-count">
          Results
          <select
            value={matchCount}
            onChange={(e) => setMatchCount(Number(e.target.value))}
            disabled={loading}
          >
            {MATCH_COUNTS.map((n) => (
              <option key={n} value={n}>
                {n}
              </option>
            ))}
          </select>
        </label>
        <button type="submit" disabled={!query.trim() || loading}>
          {loading ? "Searching…" : "Search"}
        </button>
      </form>

      {error && <p className="error">{error}</p>}

      {loading && (
        <ul className="matches" aria-hidden="true">
          {Array.from({ length: matchCount }).map((_, i) => (
            <li key={i} className="card match skeleton">
              <div className="skeleton-line short" />
              <div className="skeleton-line" />
              <div className="skeleton-line" />
            </li>
          ))}
        </ul>
      )}

      {!loading && !error && matches === null && (
        <p className="empty">
          Search across every recording you've summarized. Results are ranked
          by how closely they match.
        </p>
      )}

      {!loading && matches && matches.length === 0 && (
        <p className="empty">No matching summaries found. Try different words.</p>
      )}

      {!loading && matches && matches.length > 0 && (
        <ul className="matches">
          {matches.map((m) => (
            <MatchCard key={m.id} match={m} />
          ))}
        </ul>
      )}
    </section>
  );
}
