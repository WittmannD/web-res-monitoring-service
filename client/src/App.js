import React, { useEffect, useState } from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';

import { Container, Stack } from 'react-bootstrap';
import { observer } from 'mobx-react-lite';

import { check } from './http/api';
import LoginPage from './Routes/LoginPage';
import SignupPage from './Routes/SignupPage';
import HomePage from './Routes/HomePage';
import { useStore } from './Store/StoreProvider';
import Header from './components/Header';
import SinglePage from './Routes/SinglePage';
import MonitorEvents from './components/MonitorEvents';
import Modals from './components/Modals';

import footer from './styles/Footer.module.scss';

function App() {
  const { user } = useStore();
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    check().then((userData) => {
      if (userData) {
        user.setUser(userData);
        user.setIsAuth(true);
      }
      setIsLoading(false);
    });
  }, []);

  return !isLoading ? (
    <Stack gap={3} className="min-vh-100">
      <Header />
      <Container className="flex-fill">
        <Routes>
          <Route exact index element={<Navigate to="/dashboard" replace />} />
          <Route path="signup" replace element={<SignupPage />} />
          <Route path="login" replace element={<LoginPage />} />

          <Route
            path="dashboard"
            element={
              user.isAuth ? <HomePage /> : <Navigate to="/login" replace />
            }
          >
            <Route exact index element={<MonitorEvents />} />
            <Route path=":monitorId" element={<SinglePage />} />
          </Route>
        </Routes>
      </Container>
      <footer className={footer.footer}>
        <Container>
          <span>
            <a
              href="https://github.com/WittmannD"
              rel="nofollow noopener noreferrer"
              target="_blank"
            >
              D. Wittmann
            </a>
          </span>
        </Container>
      </footer>
      <Modals />
    </Stack>
  ) : null;
}

export default observer(App);
