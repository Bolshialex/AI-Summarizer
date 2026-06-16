import { useState } from "react";
import { summarizeFile } from "../api";
import { formatTimestamp } from "../format";
import type { SummaryResponse } from "../types";

export default function Summarizer() {
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<SummaryResponse | null>(null);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!file) return;

    setLoading(true);
    setError(null);
    setResult(null);
    try {
      setResult(await summarizeFile(file));
    } catch (err) {
      setError(err instanceof Error ? err.message : "Something went wrong");
    } finally {
      setLoading(false);
    }
  }

  return (
    <section className="panel">
      <form className="uploader" onSubmit={handleSubmit}>
        <label className="file-field">
          <input
            type="file"
            accept="audio/*,video/*"
            onChange={(e) => setFile(e.target.files?.[0] ?? null)}
            disabled={loading}
          />
          <span>{file ? file.name : "Choose an audio or video file"}</span>
        </label>
        <button type="submit" disabled={!file || loading}>
          {loading ? "Summarizing…" : "Summarize"}
        </button>
      </form>

      {loading && (
        <p className="hint">
          Transcribing and summarizing — this can take a minute for longer files.
        </p>
      )}

      {error && <p className="error">{error}</p>}

      {result && (
        <div className="result">
          <h2>{result.video_name}</h2>

          <h3>Summary</h3>
          <pre className="summary-text">{result.summary}</pre>

          {result.segments.length > 0 && (
            <details className="transcript">
              <summary>Transcript ({result.segments.length} segments)</summary>
              <ul>
                {result.segments.map((seg, i) => (
                  <li key={i}>
                    <span className="ts">{formatTimestamp(seg.start)}</span>
                    <span>{seg.text.trim()}</span>
                  </li>
                ))}
              </ul>
            </details>
          )}
        </div>
      )}
    </section>
  );
}
