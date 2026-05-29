import "../App.css";
import { Link } from "react-router-dom";

function Navbar() {
  return (
    <nav className="navbar">
      <div className="navbar-group">
        <Link to="/" className="navbar-items">
          Home
        </Link>
        <Link to="/upload" className="navbar-items">
          Upload Audio/Video
        </Link>
        <Link to="files" className="navbar-items">
          All Uploaded Files
        </Link>
      </div>
    </nav>
  );
}

export default Navbar;
