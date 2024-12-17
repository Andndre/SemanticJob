import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';

const ProtectedRoute = ({ children }: {
  children: React.ReactNode;
}) => {
  const { user } = useAuth();
  const navigate = useNavigate();

  if (!user) {
    navigate('/auth/login', { replace: true });
  }

  return <>
    { children }
  </>;
};

export default ProtectedRoute;