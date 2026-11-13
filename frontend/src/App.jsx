import { useEffect, useState } from "react";
import "./App.css";

function App() {
  const [projects, setProjects] = useState([]);
  const [profile, setProfile] = useState(null);
  const [skills, setSkills] = useState([]);

  const [formData, setFormData] = useState({
    name: "",
    email: "",
    message: "",
  });

  useEffect(() => {
    fetch("http://127.0.0.1:8000/api/projects/")
      .then((response) => response.json())
      .then((data) => {
        setProjects(data);
      })
      .catch((error) => {
        console.error("Error fetching projects:", error);
      });
    // for profiel fetch data
    fetch("http://127.0.0.1:8000/api/profile/")
      .then((response) => response.json())
      .then((data) => {
        setProfile(data);
      })
      .catch((error) => {
        console.error("Error fetching profile:", error);
      });

    // skills
    fetch("http://127.0.0.1:8000/api/skills/")
      .then((response) => response.json())
      .then((data) => {
        setSkills(data);
      })
      .catch((error) => {
        console.error("Error fetching skills:", error);
      });
  }, []);

  console.log("Skills:", skills);
  const handleSubmit = (e) => {
    e.preventDefault();

    fetch("http://127.0.0.1:8000/api/contact/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(formData),
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error("Something went wrong");
        }
        return response.json();
      })
      .then((data) => {
        alert("Message sent successfully!");
        setFormData({
          name: "",
          email: "",
          message: "",
        });
      })
      .catch((error) => {
        console.error("Error sending message:", error);
        alert("Failed to send message. Please try again.");
      });
  };

  return (
    <main>
      {/* Navigation */}
      <nav className="navbar">
        <a href="/" className="logo">
          Prashant Shah.
        </a>

        <div className="nav-links">
          <a href="#work">Work</a>
          <a href="#about">About</a>
          <a href="#skills">Skills</a>
          <a href="#contact">Contact</a>
        </div>
      </nav>

      {profile && (
        <section className="about" id="about">
          <div className="about-content">
            <p className="eyebrow">A LITTLE ABOUT ME</p>

            <h2>{profile.name}</h2>

            <h3>{profile.title}</h3>

            <p className="about-description">{profile.bio}</p>

            <div className="about-links">
              <a href={profile.github_url} target="_blank" rel="noreferrer">
                GitHub ↗
              </a>

              <a href={profile.linkedin_url} target="_blank" rel="noreferrer">
                LinkedIn ↗
              </a>
            </div>
          </div>
          {profile.profile_image && (
            <div className="about-image">
              <img
                src={`http://127.0.0.1:8000${profile.profile_image}`}
                alt={profile.name}
              />
            </div>
          )}{" "}
        </section>
      )}

      {/* Hero Section */}
      <section className="hero">
        <div className="hero-content">
          <p className="eyebrow">COMPUTER ENGINEERING STUDENT · DEVELOPER</p>

          <h1>
            Building digital
            <br />
            experiences with purpose.
          </h1>

          <p className="hero-description">
            I'm Prashant, a developer interested in building useful, thoughtful
            and meaningful digital products.
          </p>

          <div className="hero-actions">
            <a href="#work" className="primary-link">
              Explore my work ↗
            </a>

            <a href="#contact" className="secondary-link">
              Get in touch
            </a>
          </div>
        </div>
      </section>

      {/* Projects Section */}
      <section className="projects" id="work">
        <div className="section-heading">
          <p className="eyebrow">SELECTED WORK</p>
          <h2>Things I've built.</h2>
          <p>
            A collection of projects I've worked on while learning and building.
          </p>
        </div>

        {/* project grid */}
        <div className="project-grid">
          {projects.map((project) => (
            <article className="project-card" key={project.id}>
              <div className="project-image">
                {project.image && (
                  <img
                    src={`http://127.0.0.1:8000${project.image}`}
                    alt={project.title}
                  />
                )}
              </div>

              <div className="project-info">
                <div>
                  <h3>{project.title}</h3>
                  <p>{project.description}</p>
                </div>

                <p className="project-tech">
                  {project.technologies.map((skill) => skill.name).join(" · ")}
                </p>
              </div>
            </article>
          ))}
        </div>
      </section>

      {/* Skills Section to show in ui*/}
      <section className="skills" id="skills">
        <div className="section-heading">
          <p className="eyebrow">MY TOOLKIT</p>
          <h2>Technologies I work with.</h2>
        </div>

        <div className="skills-grid">
          {skills.map((skill) => (
            <div className="skill-item" key={skill.id}>
              {skill.name}
            </div>
          ))}
        </div>
      </section>

      {/* Contact Section */}
      <section className="contact" id="contact">
        <div className="section-heading">
          <p className="eyebrow">GET IN TOUCH</p>
        </div>

        <form className="contact-form" onSubmit={handleSubmit}>
          <input
            type="text"
            placeholder="Your name"
            value={formData.name}
            onChange={(e) => setFormData({ ...formData, name: e.target.value })}
          />

          <input
            type="email"
            placeholder="Your email"
            value={formData.email}
            onChange={(e) =>
              setFormData({ ...formData, email: e.target.value })
            }
          />

          <textarea
            placeholder="Your message"
            rows="5"
            value={formData.message}
            onChange={(e) =>
              setFormData({ ...formData, message: e.target.value })
            }
          />

          <button type="submit">Send message ↗</button>
        </form>
      </section>

      {/* Footer */}
      <footer className="footer">
        <p>© {new Date().getFullYear()} Prashant Shah. All rights reserved.</p>

        <div className="footer-links">
          <a href={profile?.github_url} target="_blank" rel="noreferrer">
            GitHub ↗
          </a>
          <a href={profile?.linkedin_url} target="_blank" rel="noreferrer">
            LinkedIn ↗
          </a>
        </div>
      </footer>
    </main>
  );
}

export default App;
