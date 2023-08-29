import { Button, Dropdown, Stack } from 'react-bootstrap';
import React, { useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import PropTypes from 'prop-types';

import { useStore } from '../../../Store/StoreProvider';
import { modalOptions } from '../../Modals/EditingModal';
import { dialogModalOptions } from '../../Modals/DialogModal';
import { deleteMonitor, updateMonitor } from '../../../http/api';

import styles from '../styles/ControlButtons.module.scss';

const IconButton = React.forwardRef(({ children, ...props }, ref) => (
  <Stack as={Button} direction="horizontal" gap={1} {...props} ref={ref}>
    {children}
  </Stack>
));

IconButton.propTypes = {
  children: PropTypes.node.isRequired,
};

export default function ControlButtons() {
  const { monitoring, modals } = useStore();
  const navigate = useNavigate();

  const showEditFormModal = () =>
    modals.createModal(modalOptions(monitoring.current));

  const toggleCurrentMonitor = () => {
    updateMonitor(monitoring.current.id, {
      running: !monitoring.current.running,
    })
      .then((data) => {
        monitoring.setMonitor(monitoring.current.id, data.content);
      })
      .catch((error) => {
        console.log(error.response);
      });
  };

  const deleteCurrentMonitor = () => {
    deleteMonitor(monitoring.current.id)
      .then(() => {
        navigate('/dashboard', { replace: true });
        monitoring.removeMonitor(monitoring.current.id);
      })
      .catch((error) => {
        console.log(error.response);
      });
  };

  const showConfirmationModal = () =>
    modals.createModal(
      dialogModalOptions({
        message: (
          <h6 className="p-3">
            Are you sure you want to <u>permanently delete</u> this monitor?
          </h6>
        ),
        onConfirm: () => deleteCurrentMonitor(),
        onCancel: () => {},
      })
    );

  return (
    <Stack direction="horizontal" className="ms-auto" gap={2}>
      <IconButton size="sm" onClick={showEditFormModal} variant="light">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          className="h-5 w-5"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
          strokeWidth={2}
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"
          />
        </svg>
        <span>Edit</span>
      </IconButton>
      <Dropdown>
        <Dropdown.Toggle
          as={IconButton}
          size="sm"
          variant="light"
          id="monitor-actions"
          bsPrefix="actions-toggle"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            className="h-5 w-5"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
            strokeWidth={2}
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              d="M5 12h.01M12 12h.01M19 12h.01M6 12a1 1 0 11-2 0 1 1 0 012 0zm7 0a1 1 0 11-2 0 1 1 0 012 0zm7 0a1 1 0 11-2 0 1 1 0 012 0z"
            />
          </svg>
        </Dropdown.Toggle>

        <Dropdown.Menu align="end">
          <Dropdown.Item
            as="button"
            bsPrefix={styles.action}
            onClick={showEditFormModal}
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              className="h-5 w-5"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
              strokeWidth={2}
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"
              />
            </svg>
            <span>Edit</span>
          </Dropdown.Item>
          <Dropdown.Item
            as="button"
            bsPrefix={styles.action}
            onClick={toggleCurrentMonitor}
          >
            {monitoring.current.running ? (
              <>
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  className="h-5 w-5"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                  strokeWidth={2}
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    d="M10 9v6m4-6v6m7-3a9 9 0 11-18 0 9 9 0 0118 0z"
                  />
                </svg>
                <span>Pause</span>
              </>
            ) : (
              <>
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  className="h-5 w-5"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                  strokeWidth={2}
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z"
                  />
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                  />
                </svg>
                <span>Resume</span>
              </>
            )}
          </Dropdown.Item>
          <Dropdown.Divider />
          <Dropdown.Item
            as="button"
            bsPrefix={`${styles.action} ${styles.danger}`}
            onClick={showConfirmationModal}
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              className="h-5 w-5"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
              strokeWidth={2}
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"
              />
            </svg>
            <span>Delete</span>
          </Dropdown.Item>
        </Dropdown.Menu>
      </Dropdown>
    </Stack>
  );
}
