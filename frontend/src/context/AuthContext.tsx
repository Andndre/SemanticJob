import React, { createContext, useContext, useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

interface AuthContextType {
  user: string | null;
  login: (username: string, password: string) => Promise<{ success: boolean, message: string }>;
  register: (username: string, password: string) => Promise<{ success: boolean, message: string }>;
  logout: () => void;
  loading: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    // Check if user is already logged in
    axios.get('http://localhost:5000/api/user', { withCredentials: true })
      .then(response => {
        setUser(response.data.username);
        setLoading(false);
      })
      .catch(() => {
        setUser(null);
        setLoading(false);
      });
  });

  const login = async (username: string, password: string) => {
    try {
      setLoading(true);
      await axios.post('http://localhost:5000/api/login', { username, password }, { withCredentials: true });
      setUser(username);
      navigate('/');
      return { success: true, message: 'Login successful' };
    } catch (error: any) {
      console.error('Login failed', error);
      return { success: false, message: error.response.data.error };
    } finally {
      setLoading(false);
    }
  };

  const register = async (username: string, password: string) => {
    try {
      setLoading(true);
      await axios.post('http://localhost:5000/api/register', { username, password }, { withCredentials: true });
      setUser(username);
      navigate('/auth/login');
      return { success: true, message: 'Registration successful' };
    } catch (error: any) {
      console.error('Register failed', error);
      return { success: false, message: error.response.data.error };
    } finally {
      setLoading(false);
    }
  }

  const logout = async () => {
    setLoading(true);
    await axios.post('http://localhost:5000/api/logout', {}, { withCredentials: true });
    setUser(null);
    setLoading(false);
    navigate('/auth/login');
  };

  return (
    <AuthContext.Provider value={{ user, login, logout, loading, register }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
