import React, { useEffect, useState } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { sendVerificationEmail, verifyEmail } from '../../http/api';

export default function Verification() {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const [emailVerified, setEmailVerified] = useState(false);

  useEffect(() => {
    if (searchParams.get('token')) {
      verifyEmail(searchParams.get('token')).then((data) => {
        setEmailVerified(true);

        window.setTimeout(() => navigate('/', { replace: true }), 3000);
      });
    } else {
      sendVerificationEmail().then();
    }
  }, []);

  return emailVerified ? (
    <div>
      <h5>Account successfully activated!</h5>
      <p className="subtitle">
        You will be automatically redirected to the dashboard page.
      </p>
    </div>
  ) : (
    <div>
      <h5>An activation email has been sent to your address.</h5>
    </div>
  );
}
