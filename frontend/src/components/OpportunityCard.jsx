export default function OpportunityCard({ opportunity }) {
  return (
    <div className="opportunity-card">
      <span className="badge">{opportunity.category}</span>
      <h3>{opportunity.title}</h3>
      <p className="small">Organizer: {opportunity.organizer}</p>
      <p className="small">Match score: {opportunity.match_score}/100</p>
      <p className="small">Deadline: {opportunity.deadline || 'Not listed'}</p>
      <p className="small">Location: {opportunity.location}</p>
      <p className="small">Mode: {opportunity.mode}</p>
      <p>{opportunity.description}</p>
      <p className="small">Why it matches: {opportunity.why_it_matches}</p>
      <p className="small">Source: {opportunity.source}</p>
      <div className="actions">
        <a className="btn btn-primary" href={opportunity.url} target="_blank" rel="noreferrer">View Opportunity</a>
      </div>
    </div>
  );
}
