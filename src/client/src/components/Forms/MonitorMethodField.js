import PropTypes from 'prop-types';
import { Form } from 'react-bootstrap';
import { Controller } from 'react-hook-form';
import React from 'react';

export default function MonitorMethodField({ control }) {
  return (
    <Controller
      name="method"
      control={control}
      rules={{
        required: true,
      }}
      render={({ field, fieldState: { error } }) => (
        <>
          <Form.Control
            as={Form.Select}
            aria-label="HTTP method select"
            {...field}
            isInvalid={!!error}
          >
            <option value="GET">GET</option>
            <option value="POST">POST</option>
            <option value="OPTIONS">OPTIONS</option>
          </Form.Control>
          <Form.Control.Feedback type="invalid">
            {error && error.message}
          </Form.Control.Feedback>
        </>
      )}
    />
  );
}

MonitorMethodField.propTypes = {
  control: PropTypes.objectOf(PropTypes.any).isRequired,
};
