
import { FaSun, FaMoon } from "react-icons/fa";

function Navbar({ theme, toggleTheme }) {
  return (
    <nav className="navbar">
      <a href="#home" className="logo">
        Prashant Shah.
      </a>

      <div className="nav-right">
        <div className="nav-links">
          <a href="#work">Work</a>
          <a href="#home">About</a>
          <a href="#skills">Skills</a>
          <a href="#contact">Contact</a>
        </div>

        <button
          className="theme-toggle"
          onClick={toggleTheme}
          aria-label={
            theme === "light"
              ? "Switch to dark mode"
              : "Switch to light mode"
          }
          title={
            theme === "light"
              ? "Switch to dark mode"
              : "Switch to light mode"
          }
        >
          {theme === "light" ? <FaMoon /> : <FaSun />}
        </button>
      </div>
    </nav>
  );
}

export default Navbar;
