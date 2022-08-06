import React from 'react';
import { Col, FloatingLabel, Form, Row } from 'react-bootstrap';
import moment from 'moment';
import Button from 'react-bootstrap/Button';
import { useForm, Controller } from 'react-hook-form';
import { postMonitor } from '../../http/api';
import { useStore } from '../../Store/StoreProvider';

const MONITOR_FORM_MODAL_WINDOW = 'MonitorFormModalWindow';

export function CreationModal() {
  const { monitoring, modals } = useStore();
  const { control, handleSubmit } = useForm({
    defaultValues: {
      url: '',
      method: 'GET',
      interval: 60,
    },
  });

  const onSubmit = (monitorData) => {
    postMonitor(monitorData)
      .then((data) => {
        console.log(data);
        monitoring.addMonitor(data.content);
        modals.hideModal(MONITOR_FORM_MODAL_WINDOW);
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
              rules={{
                required: true,
              }}
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
              rules={{
                required: true,
              }}
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
          rules={{
            required: true,
          }}
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
      <Button variant="primary" type="submit">
        Create
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
