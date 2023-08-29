import React, { useState } from 'react';
import PropTypes from 'prop-types';

import { Fade } from 'react-bootstrap';
import clsx from 'clsx';
import styles from './styles/Alert.module.scss';

function Alert({
  children,
  defaultShown = true,
  closable = true,
  variant = 'dark',
  onClose = null,
  ...props
}) {
  const [isShown, setIsShown] = useState(defaultShown);
  const classes = clsx(
    styles.alert,
    styles[variant],
    closable && styles.closable
  );
  return (
    <Fade in={isShown} appear={defaultShown} unmountOnExit {...props}>
      <div className={classes} role="alert">
        {closable && (
          <button
            type="button"
            aria-label="close"
            className={styles.closeButton}
            onClick={() => {
              setIsShown(false);
              onClose && onClose();
            }}
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              className="h-6 w-6"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
              strokeWidth={2}
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                d="M6 18L18 6M6 6l12 12"
              />
            </svg>
          </button>
        )}
        <div>{children}</div>
      </div>
    </Fade>
  );
}

Alert.propTypes = {
  children: PropTypes.node.isRequired,
  defaultShown: PropTypes.bool,
  closable: PropTypes.bool,
  onClose: PropTypes.func,
  variant: PropTypes.string,
};

Alert.defaultProps = {
  defaultShown: true,
  closable: true,
  onClose: null,
  variant: 'dark',
};

export default Alert;
