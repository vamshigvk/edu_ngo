import React from 'react';
import { Link } from 'react-router-dom';

function HomePage() {
  return (
    <div className="page-shell">
      <section className="hero-card">
        <div>
          <p className="badge">Role-based learning hub</p>
          <h1 className="hero-title">Support every learner with one calm, clear portal.</h1>
          <p className="hero-subtitle">
            Students, mentors, and admins can move through a light and welcoming experience with simple access to notices,
            recommendations, and guidance.
          </p>
          <div className="hero-actions">
            <Link to="/signin" className="btn btn-primary">Sign in</Link>
            <Link to="/signup" className="btn btn-secondary">Create account</Link>
          </div>
        </div>
        <div className="info-stack">
          <div className="info-pill">• Clear role-based dashboard views</div>
          <div className="info-pill">• Simple announcements and learning resources</div>
          <div className="info-pill">• Friendly onboarding for mentors and students</div>
        </div>
      </section>
    </div>
  );
}

export default HomePage;
