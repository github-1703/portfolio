
import { useEffect, useState } from "react";
import "./App.css";

import Navbar from "./components/Navbar";
import Hero from "./components/Hero";
import Projects from "./components/Projects";
import Skills from "./components/Skills";
import Contact from "./components/Contact";
import Footer from "./components/Footer";

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";

function App() {
  const [projects, setProjects] = useState([]);
  const [profile, setProfile] = useState(null);
  const [skills, setSkills] = useState([]);

  const [formData, setFormData] = useState({
    name: "",
    email: "",
    message: "",
  });

  // Dark mode state
  const [theme, setTheme] = useState(() => {
    return localStorage.getItem("portfolio-theme") || "light";
  });

  // Fetch data from Django API
  useEffect(() => {
    fetch(`${API_BASE_URL}/api/projects/`)
      .then((response) => response.json())
      .then((data) => setProjects(data))
      .catch((error) =>
        console.error("Error fetching projects:", error)
      );

    fetch(`${API_BASE_URL}/api/profile/`)
      .then((response) => response.json())
      .then((data) => setProfile(data))
      .catch((error) =>
        console.error("Error fetching profile:", error)
      );

    fetch(`${API_BASE_URL}/api/skills/`)
      .then((response) => response.json())
      .then((data) => setSkills(data))
      .catch((error) =>
        console.error("Error fetching skills:", error)
      );
  }, []);

  // Apply selected theme
  useEffect(() => {
    document.documentElement.setAttribute("data-theme", theme);
    localStorage.setItem("portfolio-theme", theme);
  }, [theme]);

  // Toggle between light and dark mode
  const toggleTheme = () => {
    setTheme((current) =>
      current === "light" ? "dark" : "light"
    );
  };

  return (
    <main>
      <Navbar theme={theme} toggleTheme={toggleTheme} />

      <Hero myprofile={profile} />

      <Projects projects={projects} />

      <Skills myskills={skills} />

      <Contact
        formData={formData}
        setFormData={setFormData}
      />

      <Footer myprofile={profile} />
    </main>
  );
}

export default App;
