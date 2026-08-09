import { Link, Outlet, useLocation } from 'react-router-dom';

export default function Layout() {
  const location = useLocation();
  const isLanding = location.pathname === '/';
  return (
    <div className="app-shell">
      <div className="container">
        <nav className="navbar">
          <Link to="/" className="brand">CareerPilot</Link>
          {!isLanding && <Link to="/" className="btn btn-secondary">Home</Link>}
        </nav>
        <Outlet />
      </div>
    </div>
  );
}
