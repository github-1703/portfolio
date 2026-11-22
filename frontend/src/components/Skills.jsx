import {
  SiPython,
  SiDjango,
  SiReact,
  SiJavascript,
  SiHtml5,
  SiCss,
  SiPostgresql,
  SiMysql,
  SiGit,
  SiDocker,
} from "react-icons/si";

import { FaCode } from "react-icons/fa6";
const skillIcons = {
  Python: SiPython,
  Django: SiDjango,
  React: SiReact,
  JavaScript: SiJavascript,
  HTML: SiHtml5,
  CSS: SiCss,
  PostgreSQL: SiPostgresql,
  SQL: SiMysql,
  Git: SiGit,
  Docker: SiDocker,
};

function Skills({myskills}) {
  
 return (
    <section className="skills" id="skills">
      <div className="section-heading">
        <p className="eyebrow">MY TOOLKIT</p>
        <h2>Technologies I work with.</h2>
        <p>
          Tools and technologies I've been learning and using to build projects.
        </p>
      </div>

      <div className="skills-grid">
        {myskills.map((skill) => {
          const Icon = skillIcons[skill.name] || FaCode;

          return (
            <div className="skill-item" key={skill.id}>
              <Icon className="skill-icon" />
              <span>{skill.name}</span>
            </div>
          );
        })}
      </div>
    </section>
  );
}

export default Skills
