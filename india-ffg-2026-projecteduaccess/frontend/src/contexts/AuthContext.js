import React, { createContext, useContext, useEffect, useMemo, useState } from 'react';
import { getCurrentUser, removeToken, setToken } from '../services/api';

const AuthContext = createContext();

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [authError, setAuthError] = useState(null);

  useEffect(() => {
    let active = true;

    async function bootstrap() {
      try {
        const data = await getCurrentUser();
        if (!active) return;
        setUser(data);
        setAuthError(null);
      } catch (error) {
        if (!active) return;
        removeToken();
        setUser(null);
        setAuthError(error.message || 'Unable to load session');
      } finally {
        if (active) {
          setLoading(false);
        }
      }
    }

    bootstrap();

    return () => {
      active = false;
    };
  }, []);

  const login = async (token, userData) => {
    setToken(token);
    setUser(userData);
    setAuthError(null);
  };

  const logout = () => {
    removeToken();
    setUser(null);
    setAuthError(null);
  };

  const value = useMemo(() => ({ user, loading, authError, login, logout }), [user, loading, authError]);

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  return useContext(AuthContext);
}
