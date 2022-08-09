import React, { useState } from 'react';
import { Col, FloatingLabel, Form, Row, Spinner } from 'react-bootstrap';
import moment from 'moment';
import Button from 'react-bootstrap/Button';
import { useForm, Controller } from 'react-hook-form';
import PropTypes from 'prop-types';
import { updateMonitor } from '../../http/api';
import { useStore } from '../../Store/StoreProvider';
import MonitorRange from '../Forms/MonitorRange';
import MonitorUrlField from '../Forms/MonitorUrlField';
import MonitorMethodField from '../Forms/MonitorMethodField';

const EDIT_FORM_MODAL_WINDOW = 'EditFormModalWindow';

export function EditingModal({ monitor }) {
  const { monitoring, modals } = useStore();
  const [isLoading, setIsLoading] = useState(false);
  const { control, handleSubmit, setError } = useForm({
    defaultValues: {
      url: monitor.url,
      method: monitor.method,
      interval: monitor.interval,
    },
  });

  const onSubmit = (monitorData) => {
    setIsLoading(true);
    updateMonitor(monitor.id, monitorData)
      .then((data) => {
        monitoring.setMonitor(monitor.id, data.content);
        modals.hideModal(EDIT_FORM_MODAL_WINDOW);
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
            <MonitorUrlField control={control} disabled />
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

EditingModal.propTypes = {
  monitor: PropTypes.objectOf(PropTypes.any).isRequired,
};

export const modalOptions = (monitor) => ({
  id: EDIT_FORM_MODAL_WINDOW,
  content: {
    body: () => <EditingModal monitor={monitor} />,
    title: () => `Edit monitor #${monitor.id}`,
  },
  options: {
    size: 'lg',
  },
});
