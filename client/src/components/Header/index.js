import { Container, Nav, Navbar, NavDropdown, NavItem } from 'react-bootstrap';
import { Link, useNavigate } from 'react-router-dom';
import React from 'react';

import { observer } from 'mobx-react-lite';
import { useStore } from '../../Store/StoreProvider';
import { logout } from '../../http/api';

import styles from './styles/Header.module.scss';

function Header() {
  const { user } = useStore();
  const navigate = useNavigate();
  const onLogout = () => {
    logout().then(() => {
      user.setUser({});
      user.setIsAuth(false);
      navigate('/auth/login', { replace: true });
    });
  };

  return (
    <header>
      <Navbar bg="light" expand="sm">
        <Container>
          <Navbar.Brand>
            <Link to="/" className={styles.brand}>
              monitoring app
            </Link>
          </Navbar.Brand>
          <Navbar.Toggle aria-controls="nav-toggle" />
          <Navbar.Collapse className="justify-content-end ps-5" id="nav-toggle">
            <Nav className="flex-fill">
              {!user.isAuth ? (
                <>
                  <NavItem className="ms-auto">
                    <Nav.Link as={Link} to="/auth/signup">
                      Sign up
                    </Nav.Link>
                  </NavItem>
                  <NavItem>
                    <Nav.Link as={Link} to="/auth/login">
                      Log in
                    </Nav.Link>
                  </NavItem>
                </>
              ) : (
                <NavDropdown
                  title={user.user.email}
                  id="nav-dropdown"
                  className="ms-auto"
                  align="end"
                >
                  <NavDropdown.Item onClick={onLogout}>
                    Log Out
                  </NavDropdown.Item>
                </NavDropdown>
              )}
            </Nav>
          </Navbar.Collapse>
        </Container>
      </Navbar>
    </header>
  );
}

export default observer(Header);
