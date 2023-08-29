import { Form } from 'react-bootstrap';
import { Controller } from 'react-hook-form';
import React from 'react';
import PropTypes from 'prop-types';

export default function MonitorUrlField({ control, disabled = false }) {
  return (
    <Controller
      name="url"
      control={control}
      rules={{
        required: true,
        disabled,
      }}
      render={({ field, fieldState: { error } }) => (
        <>
          <Form.Control
            type="text"
            isInvalid={!!error}
            disabled={disabled}
            placeholder="https://example.com/get"
            {...field}
          />
          <Form.Control.Feedback type="invalid">
            {error && error.message}
          </Form.Control.Feedback>
        </>
      )}
    />
  );
}

MonitorUrlField.propTypes = {
  control: PropTypes.objectOf(PropTypes.any).isRequired,
  disabled: PropTypes.bool,
};

MonitorUrlField.defaultProps = {
  disabled: false,
};
