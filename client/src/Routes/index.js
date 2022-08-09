import { Navigate, Route, Routes } from 'react-router-dom';
import React, { useEffect, useState } from 'react';
import { observer } from 'mobx-react-lite';
import SignupPage from './SignupPage';
import LoginPage from './LoginPage';
import HomePage from './HomePage';
import MonitorEvents from '../components/MonitorEvents';
import SinglePage from './SinglePage';
import { useStore } from '../Store/StoreProvider';
import { getUser } from '../http/api';
import AuthPage from './AuthPage';
import VerificationPage from './VerificationPage';

function AppRoutes() {
  const { user } = useStore();
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    getUser()
      .then((data) => {
        if (data) {
          user.setUser(data.content);
          user.setIsAuth(true);
        }
      })
      .catch((err) => {
        if (err.response.status === 401) {
          user.setUser({});
          user.setIsAuth(false);
        }
      })
      .finally(() => setIsLoading(false));

    return () => setIsLoading(true);
  }, [user]);

  return !isLoading ? (
    <Routes>
      <Route exact index element={<Navigate to="/dashboard" replace />} />

      <Route path="auth" element={<AuthPage />}>
        <Route path="login" element={<LoginPage />} />
        <Route path="signup" element={<SignupPage />} />
        <Route path="verification" element={<VerificationPage />} />
      </Route>

      <Route
        path="dashboard"
        element={
          user.isAuth ? <HomePage /> : <Navigate to="/auth/login" replace />
        }
      >
        <Route exact index element={<MonitorEvents />} />
        <Route path=":monitorId" element={<SinglePage />} />
      </Route>
    </Routes>
  ) : null;
}

export default observer(AppRoutes);
