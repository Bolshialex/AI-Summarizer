import "./App.css";
import Summarizer from "./components/Summarizer";
import Chat from "./components/Chat";

function App() {
  return (
    <div className="app">
      <header className="hero">
        <div className="brand">
          <span className="brand-mark" aria-hidden="true">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
              <path
                d="M12 3l1.9 4.7L18.5 9l-4.6 1.3L12 15l-1.9-4.7L5.5 9l4.6-1.3L12 3z"
                fill="currentColor"
              />
              <path
                d="M18 14l.9 2.2L21 17l-2.1.8L18 20l-.9-2.2L15 17l2.1-.8L18 14z"
                fill="currentColor"
                opacity="0.7"
              />
            </svg>
          </span>
          <span className="brand-name">Summarize AI</span>
        </div>
        <h1>Turn any recording into a searchable summary</h1>
        <p className="tagline">
          Upload audio or video, get the key points in seconds, and search
          back through everything you've summarized.
        </p>
      </header>

      <Summarizer />
      <Chat />
    </div>
  );
}

export default App;
