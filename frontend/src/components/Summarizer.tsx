import { useEffect, useRef, useState } from "react";
import { summarizeFile } from "../api";
import { formatTimestamp } from "../format";
import type { SummaryResponse } from "../types";

// Some containers (e.g. .mkv, .m4a) arrive with an empty MIME type, so fall
// back to the extension when the browser doesn't give us audio/* or video/*.
const EXTRA_EXTENSIONS = [
  ".mp3", ".wav", ".m4a", ".flac", ".ogg", ".oga", ".opus", ".aac", ".wma",
  ".mp4", ".mov", ".mkv", ".webm", ".avi", ".m4v", ".mpeg", ".mpg",
];

function isSupported(file: File): boolean {
  if (file.type.startsWith("audio/") || file.type.startsWith("video/")) {
    return true;
  }
  const name = file.name.toLowerCase();
  return EXTRA_EXTENSIONS.some((ext) => name.endsWith(ext));
}

export default function Summarizer() {
  const [file, setFile] = useState<File | null>(null);
  const [dragging, setDragging] = useState(false);
  const [loading, setLoading] = useState(false);
  const [elapsed, setElapsed] = useState(0);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<SummaryResponse | null>(null);
  const [copied, setCopied] = useState(false);
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    if (!loading) return;
    setElapsed(0);
    const started = Date.now();
    const id = setInterval(() => {
      setElapsed(Math.floor((Date.now() - started) / 1000));
    }, 1000);
    return () => clearInterval(id);
  }, [loading]);

  function pickFile(f: File | null) {
    if (f && !isSupported(f)) {
      setFile(null);
      setError("That file type isn't supported — choose an audio or video file.");
      return;
    }
    setFile(f);
    setError(null);
    setResult(null);
  }

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

  async function copySummary() {
    if (!result) return;
    await navigator.clipboard.writeText(result.summary);
    setCopied(true);
    setTimeout(() => setCopied(false), 1500);
  }

  return (
    <section className="section">
      <div className="section-head">
        <span className="eyebrow">Summarize</span>
        <h2>Upload a recording</h2>
      </div>

      <form className="card uploader" onSubmit={handleSubmit}>
        <div
          className={`dropzone${dragging ? " dragging" : ""}${file ? " has-file" : ""}`}
          onClick={() => inputRef.current?.click()}
          onDragOver={(e) => {
            e.preventDefault();
            setDragging(true);
          }}
          onDragLeave={() => setDragging(false)}
          onDrop={(e) => {
            e.preventDefault();
            setDragging(false);
            pickFile(e.dataTransfer.files?.[0] ?? null);
          }}
        >
          <input
            ref={inputRef}
            type="file"
            accept="audio/*,video/*"
            onChange={(e) => pickFile(e.target.files?.[0] ?? null)}
            disabled={loading}
          />
          <span className="dropzone-icon" aria-hidden="true">
            <svg width="26" height="26" viewBox="0 0 24 24" fill="none">
              <path
                d="M12 16V4m0 0L8 8m4-4l4 4"
                stroke="currentColor"
                strokeWidth="1.8"
                strokeLinecap="round"
                strokeLinejoin="round"
              />
              <path
                d="M4 16v2.5A1.5 1.5 0 005.5 20h13a1.5 1.5 0 001.5-1.5V16"
                stroke="currentColor"
                strokeWidth="1.8"
                strokeLinecap="round"
              />
            </svg>
          </span>
          <p className="dropzone-main">
            {file ? file.name : "Drop a file here, or click to browse"}
          </p>
          <p className="dropzone-sub">Audio or video files</p>
        </div>

        <button type="submit" disabled={!file || loading}>
          {loading ? "Summarizing…" : "Summarize"}
        </button>
      </form>

      {loading && (
        <div className="working">
          <div className="progress" aria-hidden="true">
            <span />
          </div>
          <p className="hint">
            Transcribing and summarizing — {elapsed}s elapsed. Longer files can
            take a minute or two.
          </p>
        </div>
      )}

      {error && <p className="error">{error}</p>}

      {result && (
        <div className="card result">
          <div className="result-head">
            <h3>{result.video_name}</h3>
            <button type="button" className="ghost" onClick={copySummary}>
              {copied ? "Copied" : "Copy"}
            </button>
          </div>

          <p className="summary-text">{result.summary}</p>

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
