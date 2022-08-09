import moment from 'moment';
import { Form } from 'react-bootstrap';
import { Controller } from 'react-hook-form';
import React from 'react';
import PropTypes from 'prop-types';

export default function MonitorRange({ control }) {
  return (
    <Controller
      name="interval"
      control={control}
      render={({ field, fieldState: { error } }) => {
        const interval = moment
          .duration(field.value, 'minutes')
          .humanize(false, { m: 60 * 3, h: 25 });
        const step = field.value > 60 * 3 ? 60 : 5;

        return (
          <>
            <Form.Label>Monitoring interval (every {interval})</Form.Label>
            <Form.Range
              type="range"
              {...field}
              min={10}
              max={60 * 24 + 10}
              step={step}
            />
            <Form.Control.Feedback type="invalid">
              {error && error.message}
            </Form.Control.Feedback>
          </>
        );
      }}
    />
  );
}

MonitorRange.propTypes = {
  control: PropTypes.objectOf(PropTypes.any).isRequired,
};
