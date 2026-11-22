import React from 'react'
import ProjectCard from './ProjectCard'

function Projects({projects}) {
  return (
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
            <ProjectCard key={project.id} project={project} />
          ))}
        </div>
      </section>
  )
}

export default Projects
