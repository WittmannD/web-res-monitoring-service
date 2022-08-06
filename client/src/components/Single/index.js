import { Card, Col, Fade, ListGroup, Row, Stack } from 'react-bootstrap';
import React, { useEffect, useState } from 'react';
import { Link, useParams } from 'react-router-dom';
import Badge from 'react-bootstrap/Badge';
import { observer } from 'mobx-react-lite';
import { getMonitor } from '../../http/api';
import SinglePlaceholder from './components/SinglePlaceholder';
import Charts from '../Charts';
import { useStore } from '../../Store/StoreProvider';
import ControlButtons from './components/ControlButtons';

const badgeColors = {
  UP: 'success',
  DOWN: 'danger',
  PAUSE: 'dark',
};

function SingleMonitor() {
  const { monitorId } = useParams();
  const { monitoring } = useStore();
  const [activeTab, setActiveTab] = useState('chart');
  const [isLoading, setIsLoading] = useState(true);

  const getData = async () => {
    const { content: monitorData } = await getMonitor(monitorId);
    monitoring.setCurrentMonitor(monitorData);
  };

  useEffect(() => {
    getData().then(() => setIsLoading(false));
    return () => {
      setIsLoading(true);
    };
  }, [monitorId]);

  if (isLoading) return <SinglePlaceholder />;
  // return null;

  const status = !monitoring.current.running
    ? 'PAUSE'
    : monitoring.current.status;

  return (
    <Card>
      <Card.Header className="small">
        <Link to="/">Dashboard</Link>
        {' / '}
        <span>#{monitoring.current.id}</span>
      </Card.Header>
      <Card.Body>
        <Card.Title>
          <Stack direction="horizontal" gap={2}>
            <Badge bg={badgeColors[status]}>{status}</Badge>
            <span>{monitoring.current.url}</span>
            <ControlButtons />
          </Stack>
        </Card.Title>
        <ListGroup variant="flush">
          <ListGroup.Item>
            <Row>
              <Col className="max-w-24">Interval:</Col>
              <Col>
                <span>{monitoring.current.interval}</span>
              </Col>
            </Row>
          </ListGroup.Item>
          <ListGroup.Item>
            <Row>
              <Col className="max-w-24">Method:</Col>
              <Col>
                <span>{monitoring.current.method}</span>
              </Col>
            </Row>
          </ListGroup.Item>
          <ListGroup.Item>
            <Row>
              <Col className="max-w-24">Payload:</Col>
              <Col>
                <span>None</span>
              </Col>
            </Row>
          </ListGroup.Item>
          <ListGroup.Item>
            <Row>
              <Col className="max-w-24">Headers:</Col>
              <Col>
                <span>None</span>
              </Col>
            </Row>
          </ListGroup.Item>
        </ListGroup>
        <Charts activeTab={activeTab} setActiveTab={setActiveTab} />
      </Card.Body>
    </Card>
  );
}

export default observer(SingleMonitor);
