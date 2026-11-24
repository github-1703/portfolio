
const API_BASE_URL = (
  import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000"
).replace(/\/+$/, "");

function getImageUrl(path) {
  if (!path) return null;

  // Cloudinary or other absolute image URL
  if (/^https?:\/\//i.test(path)) {
    return path;
  }

  // Local Django media path
  return `${API_BASE_URL}/${path.replace(/^\/+/, "")}`;
}

function ProjectCard({ project }) {
  const imageUrl = getImageUrl(project.image);

  return (
    <article className="project-card">
      <div className="project-image">
        {imageUrl && (
          <img
            src={imageUrl}
            alt={project.title}
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
