import React from 'react';

import { Container, Stack } from 'react-bootstrap';

import Header from './components/Header';
import Modals from './components/Modals';

import footer from './styles/Footer.module.scss';
import AppRoutes from './Routes';

export default function App() {
  return (
    <Stack gap={3} className="min-vh-100">
      <Header />
      <Container className="flex-fill d-flex flex-column">
        <AppRoutes />
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
  );
}
