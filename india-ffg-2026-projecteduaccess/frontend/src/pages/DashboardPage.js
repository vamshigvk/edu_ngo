import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { approveUser, createNotice, getNotices, getRecommendations, getResources, getUsers, removeToken } from '../services/api';

function DashboardPage({ role }) {
  const navigate = useNavigate();
  const { user, logout } = useAuth();
  const [users, setUsers] = useState([]);
  const [notices, setNotices] = useState([]);
  const [recommendations, setRecommendations] = useState([]);
  const [resources, setResources] = useState([]);
  const [title, setTitle] = useState('');
  const [body, setBody] = useState('');
  const [noticeRole, setNoticeRole] = useState(role || 'admin');

  useEffect(() => {
    async function load() {
      try {
        if (role === 'admin') {
          const data = await getUsers();
          setUsers(data);
        }
        const noticesData = await getNotices(role);
        setNotices(noticesData);
        const recData = await getRecommendations(role);
        setRecommendations(recData);
        if (role === 'student') {
          const resourceData = await getResources();
          setResources(resourceData);
        }
      } catch (error) {
        console.error(error);
      }
    }

    load();
  }, [role]);

  async function handleApprove(userId, verifiedAs) {
    try {
      await approveUser(userId, verifiedAs);
      const data = await getUsers();
      setUsers(data);
    } catch (error) {
      console.error(error);
    }
  }

  async function handleCreateNotice(e) {
    e.preventDefault();
    try {
      await createNotice({ title, body, role: noticeRole });
      const data = await getNotices(role);
      setNotices(data);
      setTitle('');
      setBody('');
    } catch (error) {
      console.error(error);
    }
  }

  function handleLogout() {
    logout();
    removeToken();
    navigate('/signin');
  }

  if (!user) return <div>Loading...</div>;

  return (
    <div className="page-shell">
      <div className="dashboard-card">
        <div className="dashboard-header">
          <div>
            <p className="badge">{role.charAt(0).toUpperCase() + role.slice(1)} workspace</p>
            <h2>{role.charAt(0).toUpperCase() + role.slice(1)} dashboard</h2>
            <p>Welcome, {user.full_name}</p>
          </div>
          <button className="btn btn-secondary" onClick={handleLogout}>Logout</button>
        </div>

        {role === 'admin' ? (
          <div className="grid-2">
            <div className="panel-card">
              <h3>Pending users</h3>
              <ul className="list">
                {users.filter((u) => u.status !== 'approved').map((u) => (
                  <li key={u.id}>
                    <strong>{u.full_name}</strong> ({u.email})<br />
                    <span>{u.role}</span>
                    <div className="inline-row">
                      <button className="btn btn-primary" onClick={() => handleApprove(u.id, u.role)}>Approve</button>
                    </div>
                  </li>
                ))}
              </ul>
            </div>
            <div className="panel-card">
              <h3>Publish notice</h3>
              <form onSubmit={handleCreateNotice} className="form-grid">
                <input className="input" placeholder="Title" value={title} onChange={(e) => setTitle(e.target.value)} />
                <input className="input" placeholder="Body" value={body} onChange={(e) => setBody(e.target.value)} />
                <select className="select" value={noticeRole} onChange={(e) => setNoticeRole(e.target.value)}>
                  <option value="admin">Admin</option>
                  <option value="mentor">Mentor</option>
                  <option value="mentee">Mentee</option>
                  <option value="student">Student</option>
                </select>
                <button className="btn btn-primary" type="submit">Publish</button>
              </form>
            </div>
          </div>
        ) : null}

        <div className="grid-2">
          <div className="panel-card">
            <h3>Notices</h3>
            <ul className="list">{notices.map((n) => <li key={n.id}><strong>{n.title}</strong>: {n.body}</li>)}</ul>
          </div>
          <div className="panel-card">
            <h3>Recommendations</h3>
            <ul className="list">{recommendations.map((r) => <li key={r.id}>{r.title}: {r.description}</li>)}</ul>
          </div>
        </div>

        {role === 'student' ? (
          <div className="panel-card">
            <h3>Resources</h3>
            <ul className="list">{resources.map((r) => <li key={r.id}>{r.title}: {r.description}</li>)}</ul>
          </div>
        ) : null}
      </div>
    </div>
  );
}

export default DashboardPage;
