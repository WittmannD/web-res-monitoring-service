import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import Form from 'react-bootstrap/Form';
import { ButtonGroup } from 'react-bootstrap';
import Button from 'react-bootstrap/Button';
import { useForm, Controller } from 'react-hook-form';
import { login } from '../../http/api';
import { useStore } from '../../Store/StoreProvider';

import './Login.css';

export default function Login() {
  const { control, handleSubmit } = useForm({
    defaultValues: {
      username: '',
      password: '',
    },
  });
  const { user } = useStore();
  const navigate = useNavigate();

  const onSubmit = async (data) => {
    const { username, password } = data;
    login(username, password)
      .then((userData) => {
        user.setUser(userData);
        user.setIsAuth(true);
        navigate('/monitoring', { replace: true });
      })
      .catch((error) => {
        console.log(error.response);
      });
  };

  return (
    <div className="Login">
      <Form onSubmit={handleSubmit(onSubmit)}>
        <Form.Group size="lg" className="mb-3" controlId="email">
          <Form.Label>Username</Form.Label>
          <Controller
            name="username"
            control={control}
            rules={{
              required: true,
            }}
            render={({ field }) => (
              <Form.Control autoFocus type="text" {...field} />
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
            render={({ field }) => <Form.Control type="password" {...field} />}
          />
        </Form.Group>
        <ButtonGroup className="d-flex mb-3">
          <Button type="submit">Login</Button>
        </ButtonGroup>
        <Form.Text>
          <Link to="/signup" replace>
            I don&apos;t have the account yet.
          </Link>
        </Form.Text>
      </Form>
    </div>
  );
}
