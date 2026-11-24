
import { FaGithub, FaLinkedin } from "react-icons/fa";

const API_BASE_URL = (
  import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000"
).replace(/\/+$/, "");

function getImageUrl(path) {
  if (!path) return null;

  if (/^https?:\/\//i.test(path)) {
    return path;
  }

  return `${API_BASE_URL}/${path.replace(/^\/+/, "")}`;
}

function Hero({ myprofile }) {
  if (!myprofile) return null;

  const profileImage = getImageUrl(myprofile.profile_image);

  return (
    <section className="hero" id="home">
      <div className="hero-content">
        <p className="eyebrow">
          COMPUTER ENGINEERING STUDENT · DEVELOPER
        </p>

        <h1>
          Hello, I'm {myprofile.name}.
        </h1>

        <h2 className="hero-title">
          {myprofile.title}
        </h2>

        <p className="hero-description">
          {myprofile.bio}
        </p>

        <div className="hero-actions">
          <a href="#work" className="primary-link">
            <span>Explore my work</span>
            <span className="link-arrow" aria-hidden="true">
              ↗
            </span>
          </a>

          <a href="#contact" className="secondary-link">
            Get in touch
          </a>
        </div>

        <div className="hero-social">
          {myprofile.github_url && (
            <a
              href={myprofile.github_url}
              target="_blank"
              rel="noopener noreferrer"
              aria-label="Visit my GitHub profile"
            >
              <FaGithub />
              <span>GitHub</span>
            </a>
          )}

          {myprofile.linkedin_url && (
            <a
              href={myprofile.linkedin_url}
              target="_blank"
              rel="noopener noreferrer"
              aria-label="Visit my LinkedIn profile"
            >
              <FaLinkedin />
              <span>LinkedIn</span>
            </a>
          )}
        </div>
      </div>

      {profileImage && (
        <div className="hero-image">
          <img
            src={profileImage}
            alt={`Portrait of ${myprofile.name}`}
          />

          <div className="hero-image-caption">
            <span></span>
            <span>Prashant Shah</span>
          </div>
        </div>
      )}
    </section>
  );
}

export default Hero;
