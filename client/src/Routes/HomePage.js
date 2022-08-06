import React from 'react';
import { Outlet } from 'react-router-dom';
import { Col, Row } from 'react-bootstrap';
import Monitors from '../components/Monitors';

export default function HomePage() {
  return (
    <Row className="g-3">
      <Col lg={4}>
        <Monitors />
      </Col>
      <Col lg={8}>
        <Outlet />
      </Col>
    </Row>
  );
}
