export default function ProjectCard({ project }) {
  return (
    <div className="project-card">
      <span className="badge">{project.category}</span>
      <h3>{project.title}</h3>
      <p className="small">Difficulty: {project.difficulty}</p>
      <p className="small">Estimated weeks: {project.estimated_weeks}</p>
      <p>{project.description}</p>
      <p className="small">Required skills: {project.required_skills.join(', ')}</p>
      <p className="small">Skills gained: {project.skills_gained.join(', ')}</p>
      <p className="small">Tech stack: {project.tech_stack.join(', ')}</p>
      <p className="small">Why it matches: {project.why_it_matches}</p>
    </div>
  );
}
