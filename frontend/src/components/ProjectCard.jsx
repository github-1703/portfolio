
import { useState } from "react";

import { getImageUrl } from "../lib/imageUrl";

function ProjectCard({ project }) {
  const [imageFailed, setImageFailed] = useState(false);

  const imageUrl =
    !imageFailed && project.image
      ? getImageUrl(project.image, { width: 900 })
      : null;

  return (
    <article className="project-card">
      <div className="project-image">
        {imageUrl && (
          <img
            src={imageUrl}
            alt={project.title}
            width="900"
            height="563"
            loading="lazy"
            decoding="async"
            onError={() => setImageFailed(true)}
          />
        )}
      </div>

      <div className="project-info">
        <div>
          <h3>{project.title}</h3>
          <p>{project.description}</p>
        </div>

        <div className="project-tech">
          {project.technologies.map((skill) => (
            <span key={skill.id}>{skill.name}</span>
          ))}
        </div>

        <div className="project-links">
          {project.github_url && (
            <a
              href={project.github_url}
              target="_blank"
              rel="noopener noreferrer"
            >
              GitHub ↗
            </a>
          )}

          {(project.live_url || project.github_url) && (
            <a
              href={project.live_url || project.github_url}
              target="_blank"
              rel="noopener noreferrer"
            >
              {project.live_url ? "Live Demo ↗" : "View on GitHub ↗"}
            </a>
          )}
        </div>
      </div>
    </article>
  );
}

export default ProjectCard;
