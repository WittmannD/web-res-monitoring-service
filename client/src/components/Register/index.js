import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import Form from 'react-bootstrap/Form';
import { ButtonGroup } from 'react-bootstrap';
import Button from 'react-bootstrap/Button';
import { Controller, useForm } from 'react-hook-form';
import { signup } from '../../http/api';

export default function Register() {
  const { control, handleSubmit, setError } = useForm({
    defaultValues: {
      email: '',
      password: '',
      password_confirmation: '',
    },
  });
  const navigate = useNavigate();

  const onSubmit = async (data) => {
    const { email, password, password_confirmation } = data;
    signup(email, password, password_confirmation)
      .then(() => {
        navigate('/auth/verification', { replace: true });
      })
      .catch((error) => {
        const { message, messages } = error.response.data;

        if (message) {
          setError('email', { message });
        }

        if (messages) {
          const { json } = messages;
          Object.entries(json).forEach(([key, values]) => {
            const messageString = values.join('; ');
            setError(key, { message: messageString });
          });
        }
      });
  };

  return (
    <div className="">
      <Form onSubmit={handleSubmit(onSubmit)}>
        <Form.Group size="lg" className="mb-3" controlId="email">
          <Form.Label>Email</Form.Label>
          <Controller
            name="email"
            control={control}
            rules={{
              required: true,
            }}
            render={({ field, fieldState: { error } }) => (
              <>
                <Form.Control
                  autoFocus
                  type="email"
                  {...field}
                  isInvalid={!!error}
                />
                <Form.Control.Feedback type="invalid">
                  {error && error.message}
                </Form.Control.Feedback>
              </>
            )}
          />
        </Form.Group>
        <Form.Group size="lg" className="mb-3" controlId="password">
          <Form.Label>Password</Form.Label>
          <Controller
            name="password"
            control={control}
            rules={{
              required: true,
            }}
            render={({ field, fieldState: { error } }) => (
              <>
                <Form.Control type="password" {...field} isInvalid={!!error} />
                <Form.Control.Feedback type="invalid">
                  {error && error.message}
                </Form.Control.Feedback>
              </>
            )}
          />
        </Form.Group>
        <Form.Group size="lg" className="mb-3" controlId="passwordConfirmation">
          <Form.Label>Password confirmation</Form.Label>
          <Controller
            name="password_confirmation"
            control={control}
            rules={{
              required: true,
            }}
            render={({ field, fieldState: { error } }) => (
              <>
                <Form.Control type="password" {...field} isInvalid={!!error} />
                <Form.Control.Feedback type="invalid">
                  {error && error.message}
                </Form.Control.Feedback>
              </>
            )}
          />
        </Form.Group>
        <ButtonGroup className="d-flex mb-3">
          <Button type="submit">Sign Up</Button>
        </ButtonGroup>
        <Form.Text>
          <Link to="/auth/login">I already have an account. Let me log in</Link>
        </Form.Text>
      </Form>
    </div>
  );
}
