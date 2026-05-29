import "./App.css";
import Main from "./layout/Main";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Home from "./pages/Home";
import Upload from "./pages/Upload";

function App() {
  return (
    <Router>
      <Routes>
        <Route element={<Main />}>
          <Route path="/" element={<Home />} />
          <Route path="/upload" element={<Upload />} />
        </Route>
      </Routes>
    </Router>
  );
}

export default App;
