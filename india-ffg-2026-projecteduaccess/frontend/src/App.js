import React from 'react';
import { Navigate, Route, Routes } from 'react-router-dom';
import { AuthProvider, useAuth } from './contexts/AuthContext';
import HomePage from './pages/HomePage';
import SignInPage from './pages/SignInPage';
import SignUpPage from './pages/SignUpPage';
import DashboardPage from './pages/DashboardPage';

function ProtectedRoute({ role, children }) {
  const { user, loading } = useAuth();

  if (loading) return <div>Loading...</div>;
  if (!user) return <Navigate to="/signin" replace />;
  if (role && user.role !== role) return <Navigate to="/signin" replace />;
  return children;
}

function AppRoutes() {
  return (
    <Routes>
      <Route path="/" element={<HomePage />} />
      <Route path="/signin" element={<SignInPage />} />
      <Route path="/signup" element={<SignUpPage />} />
      <Route path="/admin" element={<ProtectedRoute role="admin"><DashboardPage role="admin" /></ProtectedRoute>} />
      <Route path="/mentor" element={<ProtectedRoute role="mentor"><DashboardPage role="mentor" /></ProtectedRoute>} />
      <Route path="/mentee" element={<ProtectedRoute role="mentee"><DashboardPage role="mentee" /></ProtectedRoute>} />
      <Route path="/student" element={<ProtectedRoute role="student"><DashboardPage role="student" /></ProtectedRoute>} />
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}

function App() {
  return (
    <AuthProvider>
      <AppRoutes />
    </AuthProvider>
  );
}

export default App;
