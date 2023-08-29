import React from 'react';
import { Stack } from 'react-bootstrap';
import Button from 'react-bootstrap/Button';
import PropTypes from 'prop-types';

const DIALOG_MODAL_WINDOW = 'DialogModalWindow';

export function DialogModal({ message, handleClose, handleSubmit }) {
  return (
    <Stack direction="vertical" gap={2}>
      <div>{message}</div>
      <Stack direction="horizontal" gap={2}>
        <Button
          variant="secondary"
          onClick={() => handleClose()}
          className="ms-auto"
        >
          Cancel
        </Button>
        <Button variant="danger" onClick={() => handleSubmit()}>
          Confirm
        </Button>
      </Stack>
    </Stack>
  );
}

DialogModal.propTypes = {
  message: PropTypes.oneOfType([PropTypes.string, PropTypes.node]).isRequired,
  handleClose: PropTypes.func.isRequired,
  handleSubmit: PropTypes.func.isRequired,
};

export const dialogModalOptions = ({ message, onConfirm, onCancel }) => ({
  id: DIALOG_MODAL_WINDOW,
  content: {
    body: ({ handleClose, handleSubmit }) => (
      <DialogModal
        message={message}
        handleClose={handleClose}
        handleSubmit={handleSubmit}
      />
    ),
  },
  onSubmit: onConfirm,
  onClose: onCancel,
  options: {
    size: 'md',
    centered: true,
  },
});
