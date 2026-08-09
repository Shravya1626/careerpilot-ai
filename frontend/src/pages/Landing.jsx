import { Link } from 'react-router-dom';

export default function Landing() {
  return (
    <div className="hero">
      <div className="hero-card">
        <p className="badge">Powered by Gemini AI</p>
        <h1>Your Goal. Your Gap. Your Next Move.</h1>
        <p>CareerPilot uses AI to turn your current skills, experience and career goal into a personalized action plan.</p>
        <div className="actions">
          <Link className="btn btn-primary" to="/onboarding">Build My Career Path</Link>
        </div>
      </div>
      <div className="panel">
        <h3>What you get</h3>
        <div className="list">
          <div className="metric"><strong>AI analysis</strong><span>Readiness, strengths, gaps, next action</span></div>
          <div className="metric"><strong>Live opportunities</strong><span>Hackathons, internships, competitions, research, scholarships</span></div>
          <div className="metric"><strong>Personal roadmap</strong><span>Tailored projects and weekly milestones</span></div>
        </div>
      </div>
    </div>
  );
}
