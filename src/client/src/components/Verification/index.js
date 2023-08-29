import React, { useEffect, useState } from 'react';
import { Link, useNavigate, useSearchParams } from 'react-router-dom';
import { Button } from 'react-bootstrap';
import { sendVerificationEmail, verifyEmail } from '../../http/api';

export default function Verification() {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const [emailVerified, setEmailVerified] = useState(false);
  const [verificationError, setVerificationError] = useState(null);

  useEffect(() => {
    if (searchParams.get('token')) {
      verifyEmail(searchParams.get('token'))
        .then((data) => {
          setEmailVerified(true);

          window.setTimeout(() => navigate('/', { replace: true }), 3000);
        })
        .catch((error) => {
          setVerificationError(
            error.response.data && error.response.data.message
          );
        });
    } else {
      sendVerificationEmail().then();
    }
  }, []);

  if (verificationError) {
    return (
      <div className="text-center">
        <h4>Error</h4>
        <p className="subtitle">{verificationError}</p>
      </div>
    );
  }

  return emailVerified ? (
    <div className="text-center">
      <h4>Account successfully activated!</h4>
      <p className="subtitle">
        You will be automatically redirected to the dashboard page.
      </p>
    </div>
  ) : (
    <div className="text-center">
      <h4>An activation email has been sent to your address.</h4>
    </div>
  );
}
