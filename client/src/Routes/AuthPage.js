import React from 'react';
import { Outlet } from 'react-router-dom';

import styles from '../styles/Auth.module.scss';

export default function AuthPage() {
  return (
    <div className={styles.authContainer}>
      <div className={styles.imageContainer}>
        <img
          src="/62919f5487f386a1612f09738cd9b0e0.jpg"
          width="100%"
          height="100%"
          alt=""
        />
        <div className={styles.imageOverlay}>
          <h2 className={styles.title}>
            Easy to use monitoring system for your web resources.
          </h2>
        </div>
      </div>
      <div className={styles.formContainer}>
        <Outlet />
      </div>
    </div>
  );
}
