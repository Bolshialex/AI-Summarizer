import { useState } from "react";
import "./App.css";
import Summarizer from "./components/Summarizer";
import Chat from "./components/Chat";

type Tab = "summarize" | "search";

function App() {
  const [tab, setTab] = useState<Tab>("summarize");

  return (
    <main className="app">
      <h1>AI Summarizer</h1>

      <nav className="tabs">
        <button
          className={tab === "summarize" ? "active" : ""}
          onClick={() => setTab("summarize")}
        >
          Summarize
        </button>
        <button
          className={tab === "search" ? "active" : ""}
          onClick={() => setTab("search")}
        >
          Search
        </button>
      </nav>

      {tab === "summarize" ? <Summarizer /> : <Chat />}
    </main>
  );
}

export default App;
