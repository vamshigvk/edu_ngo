import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { signUp } from '../services/api';
import { useAuth } from '../contexts/AuthContext';

function SignUpPage() {
  const navigate = useNavigate();
  const { login } = useAuth();
  const [form, setForm] = useState({ full_name: '', email: '', password: '', role: 'student' });
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  async function handleSubmit(e) {
    e.preventDefault();
    setError('');
    setSuccess('');
    try {
      const data = await signUp(form);
      if (data?.token) {
        await login(data.token, data);
        setSuccess('Account created and signed in.');
        if (data.role === 'admin') navigate('/admin');
        else if (data.role === 'mentor') navigate('/mentor');
        else if (data.role === 'mentee') navigate('/mentee');
        else navigate('/student');
        return;
      }

      setSuccess('Account created. Please sign in after admin review.');
      setTimeout(() => navigate('/signin'), 1000);
    } catch (err) {
      setError(err.message || 'Signup failed');
    }
  }

  return (
    <div className="page-shell">
      <div className="auth-card">
        <p className="badge">Join the portal</p>
        <h2>Sign up</h2>
        <p>Create a profile and choose your learning role.</p>
        <form onSubmit={handleSubmit} className="form-grid">
          <input className="input" placeholder="Full name" value={form.full_name} onChange={(e) => setForm({ ...form, full_name: e.target.value })} />
          <input className="input" placeholder="Email" value={form.email} onChange={(e) => setForm({ ...form, email: e.target.value })} />
          <input className="input" type="password" placeholder="Password" value={form.password} onChange={(e) => setForm({ ...form, password: e.target.value })} />
          <select className="select" value={form.role} onChange={(e) => setForm({ ...form, role: e.target.value })}>
            <option value="mentor">Mentor</option>
            <option value="mentee">Mentee</option>
            <option value="student">Student</option>
          </select>
          <div className="form-actions">
            <button className="btn btn-primary" type="submit">Create account</button>
            <Link to="/signin">Already have an account?</Link>
          </div>
        </form>
        {error ? <p className="status-error">{error}</p> : null}
        {success ? <p className="status-success">{success}</p> : null}
      </div>
    </div>
  );
}

export default SignUpPage;
