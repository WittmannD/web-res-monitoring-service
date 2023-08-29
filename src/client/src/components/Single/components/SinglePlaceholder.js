import { Card, ListGroup, Placeholder, Stack } from 'react-bootstrap';
import React from 'react';
import RequestsListPlaceholder from '../../Charts/components/RequestsListPlaceholder';
import ChartPlaceholder from '../../Charts/components/ChartPlaceholder';

export default function SinglePlaceholder() {
  return (
    <Card>
      <Card.Header>
        <Placeholder animation="glow">
          <Placeholder xs={2} bg="secondary" />
        </Placeholder>
      </Card.Header>
      <Card.Body>
        <Placeholder as={Card.Title} animation="glow">
          <Stack direction="horizontal" gap={2}>
            <Placeholder xs={1} bg="success" />
            <Placeholder xs={2} bg="secondary" />
            <Placeholder.Button
              xs={1}
              bsPrefix="placeholder btn-sm"
              className="ms-auto"
              aria-hidden="true"
              variant="secondary"
            />
          </Stack>
        </Placeholder>
        <Placeholder as={ListGroup} animation="glow" variant="flush">
          <ListGroup.Item>
            <Placeholder xs={1} bg="secondary" />{' '}
            <Placeholder xs={2} bg="secondary" />
          </ListGroup.Item>
          <ListGroup.Item>
            <Placeholder xs={1} bg="secondary" />{' '}
            <Placeholder xs={3} bg="secondary" />
          </ListGroup.Item>
          <ListGroup.Item>
            <Placeholder xs={1} bg="secondary" />{' '}
            <Placeholder xs={2} bg="secondary" />
          </ListGroup.Item>
          <ListGroup.Item>
            <Placeholder xs={1} bg="secondary" />{' '}
            <Placeholder xs={3} bg="secondary" />
          </ListGroup.Item>
        </Placeholder>
        <Stack gap={3} className="mt-3">
          <Placeholder
            as={Stack}
            direction="horizontal"
            gap={2}
            animation="glow"
          >
            <Placeholder.Button xs={1} aria-hidden="true" variant="light" />
            <Placeholder.Button xs={2} aria-hidden="true" variant="light" />
          </Placeholder>
          <ChartPlaceholder />
        </Stack>
      </Card.Body>
    </Card>
  );
}
