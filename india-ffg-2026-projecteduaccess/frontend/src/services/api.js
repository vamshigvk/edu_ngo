const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://127.0.0.1:8000';

async function request(path, options = {}) {
  const headers = {
    'Content-Type': 'application/json',
    ...(options.headers || {}),
  };

  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...options,
    headers,
  });

  const text = await response.text();
  let data = {};
  try {
    data = text ? JSON.parse(text) : {};
  } catch {
    data = {};
  }

  if (!response.ok) {
    throw new Error(data.detail || data.message || 'Request failed');
  }
  return data;
}

export function getToken() {
  return typeof window !== 'undefined' ? localStorage.getItem('token') : null;
}

export function setToken(token) {
  if (typeof window !== 'undefined') {
    localStorage.setItem('token', token);
  }
}

export function removeToken() {
  if (typeof window !== 'undefined') {
    localStorage.removeItem('token');
  }
}

export function signIn(payload) {
  return request('/auth/signin', {
    method: 'POST',
    body: JSON.stringify(payload),
  });
}

export function signUp(payload) {
  return request('/auth/signup', {
    method: 'POST',
    body: JSON.stringify(payload),
  });
}

export function getCurrentUser() {
  const token = getToken();
  if (!token) return Promise.resolve(null);
  return request('/me', {
    headers: { Authorization: `Bearer ${token}` },
  });
}

export function getUsers() {
  const token = getToken();
  return request('/users', {
    headers: { Authorization: `Bearer ${token}` },
  });
}

export function getNotices(role) {
  const query = role ? `?role=${role}` : '';
  return request(`/notices${query}`);
}

export function getRecommendations(role) {
  const query = role ? `?role=${role}` : '';
  return request(`/recommendations${query}`);
}

export function getResources() {
  return request('/resources');
}

export function createNotice(payload) {
  const token = getToken();
  return request('/notices', {
    method: 'POST',
    headers: { Authorization: `Bearer ${token}` },
    body: JSON.stringify(payload),
  });
}

export function approveUser(userId, verifiedAs) {
  const token = getToken();
  return request(`/users/${userId}/approve`, {
    method: 'PUT',
    headers: { Authorization: `Bearer ${token}` },
    body: JSON.stringify({ verified_as: verifiedAs }),
  });
}
