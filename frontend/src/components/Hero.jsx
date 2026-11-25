
import { useState } from "react";
import { FaGithub, FaLinkedin } from "react-icons/fa";

import { getImageSrcSet, getImageUrl } from "../lib/imageUrl";

const FALLBACK_IMAGE = "/images/profile.jpg";

const fallbackProfile = {
  name: "Prashant Shah",
  title: "Computer Engineering Student / Aspiring Backend Developer",
  bio: "",
  profile_image: FALLBACK_IMAGE,
  github_url: "https://github.com/github-1703",
  linkedin_url: "https://www.linkedin.com/in/prashant-shah-695668253/",
};

function Hero({ myprofile }) {
  const profile = myprofile || fallbackProfile;

  const [imageFailed, setImageFailed] = useState(false);

  const imageUrl =
    !imageFailed && profile.profile_image
      ? getImageUrl(profile.profile_image, { width: 440 })
      : FALLBACK_IMAGE;

  // 1x (440w) and 2x (880w) variants so the portrait stays sharp on retina
  // and high-density phone screens.
  const imageSrcSet =
    !imageFailed && profile.profile_image
      ? getImageSrcSet(profile.profile_image, [440, 880])
      : undefined;

  return (
    <section className="hero" id="home">
      <div className="hero-content">
        <p className="eyebrow">
          COMPUTER ENGINEERING STUDENT · DEVELOPER
        </p>

        <h1>Hello, I'm {profile.name}.</h1>

        <h2 className="hero-title">{profile.title}</h2>

        {profile.bio && (
          <p className="hero-description">{profile.bio}</p>
        )}

        <div className="hero-actions">
          <a href="#work" className="primary-link">
            <span>Explore my work</span>
            <span className="link-arrow" aria-hidden="true">↗</span>
          </a>

          <a href="#contact" className="secondary-link">
            Get in touch
          </a>
        </div>

        <div className="hero-social">
          {profile.github_url && (
            <a
              href={profile.github_url}
              target="_blank"
              rel="noopener noreferrer"
              aria-label="Visit my GitHub profile"
            >
              <FaGithub />
              <span>GitHub</span>
            </a>
          )}

          {profile.linkedin_url && (
            <a
              href={profile.linkedin_url}
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

      <div className="hero-image">
        <img
          src={imageUrl}
          srcSet={imageSrcSet}
          sizes="(max-width: 900px) 90vw, 440px"
          alt={`Portrait of ${profile.name}`}
          fetchPriority="high"
          decoding="async"
          onError={() => setImageFailed(true)}
        />

        <div className="hero-image-caption">
          <span></span>
          <span>{profile.name}</span>
        </div>
      </div>
    </section>
  );
}

export default Hero;
