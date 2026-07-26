import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { signIn } from '../services/api';
import { useAuth } from '../contexts/AuthContext';

function SignInPage() {
  const navigate = useNavigate();
  const { login } = useAuth();
  const [form, setForm] = useState({ email: '', password: '' });
  const [error, setError] = useState('');

  async function handleSubmit(e) {
    e.preventDefault();
    setError('');
    try {
      const data = await signIn(form);
      if (!data?.token) {
        throw new Error('Authentication token missing');
      }
      await login(data.token, data);
      if (data.role === 'admin') navigate('/admin');
      else if (data.role === 'mentor') navigate('/mentor');
      else if (data.role === 'mentee') navigate('/mentee');
      else navigate('/student');
    } catch (err) {
      setError(err.message || 'Login failed');
    }
  }

  return (
    <div className="page-shell">
      <div className="auth-card">
        <p className="badge">Welcome back</p>
        <h2>Sign in</h2>
        <p>Access your learning dashboard with a secure sign in.</p>
        <form onSubmit={handleSubmit} className="form-grid">
          <input className="input" placeholder="Email" value={form.email} onChange={(e) => setForm({ ...form, email: e.target.value })} />
          <input className="input" type="password" placeholder="Password" value={form.password} onChange={(e) => setForm({ ...form, password: e.target.value })} />
          <div className="form-actions">
            <button className="btn btn-primary" type="submit">Sign in</button>
            <Link to="/signup">Create an account</Link>
          </div>
        </form>
        {error ? <p className="status-error">{error}</p> : null}
      </div>
    </div>
  );
}

export default SignInPage;
