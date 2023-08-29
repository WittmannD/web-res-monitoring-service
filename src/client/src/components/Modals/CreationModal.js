import React, { useState } from 'react';
import { Col, FloatingLabel, Form, Row, Spinner } from 'react-bootstrap';
import Button from 'react-bootstrap/Button';
import { useForm } from 'react-hook-form';
import { postMonitor } from '../../http/api';
import { useStore } from '../../Store/StoreProvider';
import MonitorRange from '../Forms/MonitorRange';
import MonitorUrlField from '../Forms/MonitorUrlField';
import MonitorMethodField from '../Forms/MonitorMethodField';

const MONITOR_FORM_MODAL_WINDOW = 'MonitorFormModalWindow';

export function CreationModal() {
  const { monitoring, modals } = useStore();
  const [isLoading, setIsLoading] = useState(false);
  const { control, handleSubmit, setError } = useForm({
    defaultValues: {
      url: '',
      method: 'GET',
      interval: 60,
    },
  });

  const onSubmit = (monitorData) => {
    setIsLoading(true);
    postMonitor(monitorData)
      .then((data) => {
        monitoring.addMonitor(data.content);
        modals.hideModal(MONITOR_FORM_MODAL_WINDOW);
      })
      .catch((error) => {
        const { message, messages } = error.response.data;

        if (message) {
          setError('url', { message });
        }

        if (messages) {
          const { json } = messages;
          Object.entries(json).forEach(([key, values]) => {
            const messageString = values.join('; ');
            setError(key, { message: messageString });
          });
        }
      })
      .finally(() => setIsLoading(false));
  };

  return (
    <Form onSubmit={handleSubmit(onSubmit)}>
      <Row className="mb-3 g-3">
        <Col sm={4}>
          <FloatingLabel controlId="method" label="Method">
            <MonitorMethodField control={control} />
          </FloatingLabel>
        </Col>
        <Col sm={8}>
          <FloatingLabel controlId="url" label="URL">
            <MonitorUrlField control={control} />
          </FloatingLabel>
        </Col>
      </Row>
      <Form.Group className="mb-3" controlId="interval">
        <MonitorRange control={control} />
      </Form.Group>
      <Button variant="primary" type="submit" disabled={isLoading}>
        {isLoading ? (
          <Spinner
            size="sm"
            as="span"
            role="status"
            animation="border"
            aria-hidden="true"
          />
        ) : (
          <span>Save</span>
        )}
      </Button>
    </Form>
  );
}

export const modalOptions = () => ({
  id: MONITOR_FORM_MODAL_WINDOW,
  content: {
    body: () => <CreationModal />,
    title: () => 'New monitor',
  },
  options: {
    size: 'lg',
  },
});
