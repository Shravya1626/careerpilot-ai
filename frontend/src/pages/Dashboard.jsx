import { useEffect, useMemo, useState } from 'react';
import { generateProjects, generateRoadmap, searchOpportunities } from '../api';
import LoadingState from '../components/LoadingState';
import OpportunityCard from '../components/OpportunityCard';
import ProjectCard from '../components/ProjectCard';

const opportunityCategories = ['all', 'hackathon', 'internship', 'competition', 'research', 'scholarship'];

export default function Dashboard() {
  const [profile, setProfile] = useState(null);
  const [analysis, setAnalysis] = useState(null);
  const [opportunities, setOpportunities] = useState([]);
  const [projects, setProjects] = useState([]);
  const [roadmap, setRoadmap] = useState([]);
  const [activeCategory, setActiveCategory] = useState('all');
  const [loading, setLoading] = useState(false);
  const [opLoading, setOpLoading] = useState(false);
  const [projectLoading, setProjectLoading] = useState(false);
  const [roadmapLoading, setRoadmapLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    const savedProfile = localStorage.getItem('careerpilot-profile');
    const savedAnalysis = localStorage.getItem('careerpilot-analysis');
    if (savedProfile) setProfile(JSON.parse(savedProfile));
    if (savedAnalysis) setAnalysis(JSON.parse(savedAnalysis));
  }, []);

  const targetWeeks = useMemo(() => profile?.target_weeks || '', [profile]);

  const loadOpportunities = async (category = activeCategory) => {
    if (!profile) return;
    setOpLoading(true);
    setError('');
    try {
      const response = await searchOpportunities(profile, category, { loading: setOpLoading, errorHandler: setError });
      const items = response.opportunities || [];
      setOpportunities(items);
    } catch (err) {
      setOpportunities([]);
      setError(err.message || "Couldn't fetch live opportunities right now.");
    }
  };

  const loadProjects = async () => {
    if (!profile || !analysis) return;
    setProjectLoading(true);
    setError('');
    try {
      const response = await generateProjects(profile, analysis, { loading: setProjectLoading, errorHandler: setError });
      setProjects(response.projects || []);
    } catch (err) {
      setProjects([]);
      setError(err.message || "CareerPilot couldn't reach Gemini right now.");
    }
  };

  const loadRoadmap = async () => {
    if (!profile || !analysis) return;
    setRoadmapLoading(true);
    setError('');
    try {
      const response = await generateRoadmap(profile, analysis, { loading: setRoadmapLoading, errorHandler: setError });
      setRoadmap(response.roadmap || []);
    } catch (err) {
      setRoadmap([]);
      setError(err.message || "CareerPilot couldn't reach Gemini right now.");
    }
  };

  if (!profile || !analysis) {
    return <div className="panel">Please complete onboarding first.</div>;
  }

  return (
    <div className="dashboard-grid">
      <div>
        <div className="panel">
          <h2>Welcome back, {profile.name || 'student'}</h2>
          <p className="small">{profile.target_role || 'Your next step is ready.'}</p>
          <div className="section">
            <h3>Career Readiness</h3>
            <p>{analysis.readiness}%</p>
            <p>{analysis.summary}</p>
          </div>
          <div className="section">
            <h3>Strengths</h3>
            <div className="chip-row">{analysis.strengths.map((item) => <span className="chip" key={item}>{item}</span>)}</div>
          </div>
          <div className="section">
            <h3>Skill Gaps</h3>
            <div className="chip-row">{analysis.skill_gaps.map((item) => <span className="chip" key={item}>{item}</span>)}</div>
          </div>
          <div className="section">
            <h3>Priority Skills</h3>
            <div className="chip-row">{analysis.priority_skills.map((item) => <span className="chip" key={item}>{item}</span>)}</div>
          </div>
          <div className="section">
            <h3>Your next best action</h3>
            <p>{analysis.next_action}</p>
            <p className="small">{analysis.reason}</p>
          </div>
        </div>

        <div className="panel">
          <div className="actions">
            <button className="btn btn-primary" onClick={loadProjects}>Generate Projects</button>
            <button className="btn btn-secondary" onClick={loadRoadmap}>Generate Roadmap</button>
          </div>
          {projectLoading ? <LoadingState message="Gemini is designing projects for your career goal..." /> : null}
          {projectLoading ? null : projects.length === 0 ? <p className="empty">No personalized projects generated yet.</p> : <div className="list">{projects.map((project) => <ProjectCard key={project.title} project={project} />)}</div>}

          {roadmapLoading ? <LoadingState message="Building your personalized roadmap..." /> : null}
          {!roadmapLoading && roadmap.length === 0 ? null : null}
          {roadmap.length > 0 ? <div className="section"><h3>{targetWeeks}-Week Career Roadmap</h3><div className="list">{roadmap.map((item) => <div className="opportunity-card" key={item.week}><strong>Week {item.week}: {item.title}</strong><p>{item.goal}</p><ul>{item.tasks.map((task) => <li key={task}>{task}</li>)}</ul><p className="small">Deliverable: {item.deliverable}</p></div>)}</div></div> : null}
        </div>
      </div>

      <div>
        <div className="panel">
          <h3>Live Opportunities</h3>
          <div className="actions">
            <button className="btn btn-primary" onClick={() => loadOpportunities(activeCategory)}>Find Opportunities</button>
            <button className="btn btn-secondary" onClick={() => loadOpportunities(activeCategory)}>Refresh Opportunities</button>
          </div>
          <div className="chip-row" style={{ marginTop: 12 }}>
            {opportunityCategories.map((category) => (
              <button type="button" key={category} className={`chip ${activeCategory === category ? 'active' : ''}`} onClick={() => setActiveCategory(category)}>{category}</button>
            ))}
          </div>
          {opLoading ? <LoadingState message="Searching the web for current opportunities..." /> : null}
          {!opLoading && opportunities.length === 0 ? <p className="empty">No opportunities loaded yet.</p> : null}
          {!opLoading && opportunities.length > 0 ? <div className="list" style={{ marginTop: 12 }}>{opportunities.map((item) => <OpportunityCard key={item.title + item.url} opportunity={item} />)}</div> : null}
          {error ? <div className="error">{error}</div> : null}
        </div>
      </div>
    </div>
  );
}
