import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import Form from 'react-bootstrap/Form';
import { ButtonGroup } from 'react-bootstrap';
import Button from 'react-bootstrap/Button';
import { useForm, Controller } from 'react-hook-form';
import { login } from '../../http/api';
import { useStore } from '../../Store/StoreProvider';

export default function Login() {
  const { control, handleSubmit, setError } = useForm({
    defaultValues: {
      email: '',
      password: '',
    },
  });
  const { user } = useStore();
  const navigate = useNavigate();

  const onSubmit = async (data) => {
    const { email, password } = data;
    login(email, password)
      .then((userData) => {
        user.setUser(userData);
        user.setIsAuth(true);
        navigate('/dashboard', { replace: true });
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
        <ButtonGroup className="d-flex mb-3">
          <Button type="submit">Login</Button>
        </ButtonGroup>
        <Form.Text>
          <Link to="/auth/signup" replace>
            I don&apos;t have the account yet.
          </Link>
        </Form.Text>
      </Form>
    </div>
  );
}
