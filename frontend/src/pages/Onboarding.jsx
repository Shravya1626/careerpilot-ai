import { useMemo, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { analyzeProfile } from '../api';

const skillOptions = [
  'Python', 'C', 'C++', 'Java', 'JavaScript', 'React', 'Node.js', 'SQL', 'Git/GitHub', 'Machine Learning', 'Deep Learning', 'Data Science', 'Cloud', 'Cybersecurity', 'IoT', 'Embedded Systems', 'MATLAB', 'Arduino', 'ESP32', 'Communication', 'Leadership', 'UI/UX'
];

const stepTitles = ['Student Information', 'Skills', 'Experience', 'Career Goal', 'Timeline'];

const initialProfile = {
  name: '',
  college: '',
  branch: '',
  year: '',
  cgpa: '',
  skills: [],
  projects: 0,
  hackathons: 0,
  internships: 0,
  target_role: '',
  dream_company: '',
  domain: '',
  work_type: '',
  weekly_hours: '',
  target_weeks: ''
};

export default function Onboarding() {
  const navigate = useNavigate();
  const [step, setStep] = useState(0);
  const [profile, setProfile] = useState(initialProfile);
  const [customSkill, setCustomSkill] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const progress = useMemo(() => ((step + 1) / 5) * 100, [step]);

  const updateField = (field, value) => setProfile((prev) => ({ ...prev, [field]: value }));

  const toggleSkill = (skill) => {
    setProfile((prev) => ({
      ...prev,
      skills: prev.skills.includes(skill) ? prev.skills.filter((item) => item !== skill) : [...prev.skills, skill]
    }));
  };

  const addCustomSkill = () => {
    const trimmed = customSkill.trim();
    if (!trimmed) return;
    setProfile((prev) => ({ ...prev, skills: prev.skills.includes(trimmed) ? prev.skills : [...prev.skills, trimmed] }));
    setCustomSkill('');
  };

  const next = () => {
    if (step < 4) {
      setStep(step + 1);
      setError('');
      return;
    }
    handleSubmit();
  };

  const previous = () => {
    if (step > 0) setStep(step - 1);
  };

  const handleSubmit = async () => {
    setLoading(true);
    setError('');
    try {
      const analysis = await analyzeProfile(profile, { loading: setLoading, errorHandler: setError });
      localStorage.setItem('careerpilot-profile', JSON.stringify(profile));
      localStorage.setItem('careerpilot-analysis', JSON.stringify(analysis));
      navigate('/dashboard');
    } catch (err) {
      setError(err.message || 'CareerPilot couldn\'t reach Gemini right now.');
    }
  };

  const renderStep = () => {
    switch (step) {
      case 0:
        return (
          <div className="form-grid">
            <div className="field"><label>Name</label><input value={profile.name} placeholder="XXX" onChange={(e) => updateField('name', e.target.value)} /></div>
            <div className="field"><label>College</label><input value={profile.college} placeholder="e.g. Presidency University" onChange={(e) => updateField('college', e.target.value)} /></div>
            <div className="field"><label>Branch</label><input value={profile.branch} placeholder="e.g. Electrical and Electronics Engineering" onChange={(e) => updateField('branch', e.target.value)} /></div>
            <div className="field"><label>Year</label><input value={profile.year} placeholder="e.g. 3rd year" onChange={(e) => updateField('year', e.target.value)} /></div>
            <div className="field"><label>CGPA</label><input value={profile.cgpa} placeholder="e.g. 8.7" onChange={(e) => updateField('cgpa', e.target.value)} /></div>
          </div>
        );
      case 1:
        return (
          <div>
            <div className="chip-row">
              {skillOptions.map((skill) => (
                <button type="button" key={skill} className={`chip ${profile.skills.includes(skill) ? 'active' : ''}`} onClick={() => toggleSkill(skill)}>{skill}</button>
              ))}
            </div>
            <div className="field" style={{ marginTop: 16 }}>
              <label>Custom skill</label>
              <div className="actions">
                <input value={customSkill} placeholder="Add another skill" onChange={(e) => setCustomSkill(e.target.value)} />
                <button type="button" className="btn btn-secondary" onClick={addCustomSkill}>Add</button>
              </div>
            </div>
          </div>
        );
      case 2:
        return (
          <div className="form-grid">
            <div className="field"><label>Projects completed</label><input type="number" min="0" value={profile.projects} onChange={(e) => updateField('projects', Number(e.target.value))} /></div>
            <div className="field"><label>Hackathons attended</label><input type="number" min="0" value={profile.hackathons} onChange={(e) => updateField('hackathons', Number(e.target.value))} /></div>
            <div className="field"><label>Internships completed</label><input type="number" min="0" value={profile.internships} onChange={(e) => updateField('internships', Number(e.target.value))} /></div>
          </div>
        );
      case 3:
        return (
          <div className="form-grid">
            <div className="field"><label>Target Role</label><input value={profile.target_role} placeholder="e.g. AI Engineer" onChange={(e) => updateField('target_role', e.target.value)} /></div>
            <div className="field"><label>Dream Company</label><input value={profile.dream_company} placeholder="e.g. Google" onChange={(e) => updateField('dream_company', e.target.value)} /></div>
            <div className="field"><label>Domain</label><input value={profile.domain} placeholder="e.g. AI / Software / Embedded / Cybersecurity" onChange={(e) => updateField('domain', e.target.value)} /></div>
            <div className="field"><label>Work Type</label><input value={profile.work_type} placeholder="e.g. Full-time / Internship / Research" onChange={(e) => updateField('work_type', e.target.value)} /></div>
          </div>
        );
      case 4:
        return (
          <div className="form-grid">
            <div className="field"><label>Weekly Hours</label><select value={profile.weekly_hours} onChange={(e) => updateField('weekly_hours', e.target.value)}><option value="">Select</option><option>3-5</option><option>5-10</option><option>10-15</option><option>15+</option></select></div>
            <div className="field"><label>How many weeks are you targeting?</label><select value={profile.target_weeks} onChange={(e) => updateField('target_weeks', e.target.value)}><option value="">Select</option><option>4 weeks</option><option>8 weeks</option><option>12 weeks</option><option>16 weeks</option><option>24 weeks</option><option>52 weeks</option></select></div>
          </div>
        );
      default:
        return null;
    }
  };

  return (
    <div className="wizard-card">
      <div className="stepper">
        <strong>Step {step + 1} / 5</strong>
        <span>{stepTitles[step]}</span>
      </div>
      <div className="progress-bar">
        <div className="progress-fill" style={{ width: `${progress}%` }} />
      </div>
      {renderStep()}
      {error ? <div className="error">{error}</div> : null}
      {loading ? <div className="loading-state">Gemini is analyzing your career path...</div> : null}
      <div className="actions" style={{ marginTop: 20 }}>
        <button className="btn btn-secondary" onClick={previous} disabled={step === 0}>Back</button>
        <button className="btn btn-primary" onClick={next}>{step === 4 ? 'Analyze My Career' : 'Next'}</button>
      </div>
    </div>
  );
}
