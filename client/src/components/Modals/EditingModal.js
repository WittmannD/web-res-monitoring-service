import React, { useState } from 'react';
import { Col, FloatingLabel, Form, Row, Spinner } from 'react-bootstrap';
import moment from 'moment';
import Button from 'react-bootstrap/Button';
import { useForm, Controller } from 'react-hook-form';
import PropTypes from 'prop-types';
import { updateMonitor } from '../../http/api';
import { useStore } from '../../Store/StoreProvider';

const EDIT_FORM_MODAL_WINDOW = 'EditFormModalWindow';

export function EditingModal({ monitor }) {
  const { monitoring, modals } = useStore();
  const [isLoading, setIsLoading] = useState(false);
  const { control, handleSubmit } = useForm({
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
        console.log(error.response);
      });
  };

  return (
    <Form onSubmit={handleSubmit(onSubmit)}>
      <Row className="mb-3 g-3">
        <Col sm={4}>
          <FloatingLabel controlId="method" label="Method">
            <Controller
              name="method"
              control={control}
              render={({ field }) => (
                <Form.Select aria-label="HTTP method select" {...field}>
                  <option value="GET">GET</option>
                  <option value="POST">POST</option>
                  <option value="OPTIONS">OPTIONS</option>
                </Form.Select>
              )}
            />
          </FloatingLabel>
        </Col>
        <Col sm={8}>
          <FloatingLabel controlId="url" label="URL">
            <Controller
              name="url"
              control={control}
              render={({ field }) => (
                <Form.Control
                  type="text"
                  placeholder="https://example.com/get"
                  {...field}
                />
              )}
            />
          </FloatingLabel>
        </Col>
      </Row>
      <Form.Group className="mb-3" controlId="interval">
        <Controller
          name="interval"
          control={control}
          render={({ field }) => {
            const interval = moment
              .duration(field.value, 'minutes')
              .humanize(false, { m: 60 * 3, h: 24 });
            const step = field.value >= 60 * 3 ? 60 : 5;

            return (
              <>
                <Form.Label>Monitoring interval (every {interval})</Form.Label>
                <Form.Range {...field} min={5} max={60 * 24} step={step} />
              </>
            );
          }}
        />
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
