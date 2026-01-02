import { Link, NavLink } from "react-router-dom";
import logo from "../assets/logo.png";

export default function Navbar() {
  return (
    <header className="navbar">
      <div className="nav-left">
        {/* Logo also acts as Home */}
        <Link to="/" className="brand">
          <img src={logo} alt="AushadhiSetu" className="brand-logo" />
          <div className="brand-text">
            <span className="brand-title">AushadhiSetu</span>
            <span className="brand-sub">Bridging Health & Savings</span>
          </div>
        </Link>
      </div>

      <nav className="nav-right">
        {/* Home button */}
        <NavLink
          to="/"
          className={({ isActive }) =>
            isActive ? "btn btn-primary" : "btn btn-ghost"
          }
        >
          Home
        </NavLink>

        <NavLink
          to="/upload"
          className={({ isActive }) =>
            isActive ? "btn btn-primary" : "btn btn-ghost"
          }
        >
          Scan
        </NavLink>

        <NavLink
          to="/results"
          className={({ isActive }) =>
            isActive ? "btn btn-primary" : "btn btn-ghost"
          }
        >
          Results
        </NavLink>

        <NavLink
          to="/about"
          className={({ isActive }) =>
            isActive ? "btn btn-primary" : "btn btn-ghost"
          }
        >
          About
        </NavLink>
      </nav>
    </header>
  );
}
