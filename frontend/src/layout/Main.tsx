import Navbar from "./NavBar";
import { Outlet } from "react-router-dom";
import "../App.css";

function Main() {
  return (
    <div className="page">
      <div>
        <Navbar />
      </div>
      <main className="main">
        <Outlet />
      </main>
    </div>
  );
}

export default Main;
