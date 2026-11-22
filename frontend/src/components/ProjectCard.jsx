function ProjectCard({ project }) {
  return (
    <article className="project-card">
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
