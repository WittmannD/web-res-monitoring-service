import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import Form from 'react-bootstrap/Form';
import { ButtonGroup } from 'react-bootstrap';
import Button from 'react-bootstrap/Button';
import { Controller, useForm } from 'react-hook-form';
import { signup } from '../../http/api';
import { useStore } from '../../Store/StoreProvider';

import './Register.css';

export default function Register() {
  const { control, handleSubmit } = useForm({
    defaultValues: {
      username: '',
      password: '',
      passwordConfirmation: '',
    },
  });
  const { user } = useStore();
  const navigate = useNavigate();

  const onSubmit = async (data) => {
    const { username, password, passwordConfirmation } = data;
    signup(username, password, passwordConfirmation)
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
    <div className="Signup">
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
        <Form.Group size="lg" className="mb-3" controlId="passwordConfirmation">
          <Form.Label>Password confirmation</Form.Label>
          <Controller
            name="passwordConfirmation"
            control={control}
            rules={{
              required: true,
            }}
            render={({ field }) => <Form.Control type="password" {...field} />}
          />
        </Form.Group>
        <ButtonGroup className="d-flex mb-3">
          <Button type="submit">Sign Up</Button>
        </ButtonGroup>
        <Form.Text>
          <Link to="/login">I already have an account. Let me log in</Link>
        </Form.Text>
      </Form>
    </div>
  );
}
