import jwtDecode from 'jwt-decode';
import { $authHost, $host } from './index';

export const signup = async (email, password, password_confirmation) => {
  const { data } = await $host.post('auth/signup', {
    email,
    password,
    password_confirmation,
  });

  if (data) {
    const token = data.content.access_token;
    localStorage.setItem('accessToken', token);
  }

  return null;
};

export const login = async (email, password) => {
  const { data } = await $host.post('auth/login', { email, password });

  const token = data.content.access_token;
  localStorage.setItem('accessToken', token);
  return jwtDecode(token);
};

export const sendVerificationEmail = async () => {
  const { data } = await $authHost.post('auth/send-verification-email');
  return data;
};

export const verifyEmail = async (token) => {
  const { data } = await $authHost.post(`auth/verify-email?token=${token}`);
  return data;
};

export const getUser = async () => {
  const { data } = await $authHost.get('user');
  return data;
};

export const logout = async () => {
  localStorage.removeItem('accessToken');
};

export const getMonitors = async () => {
  const { data } = await $authHost.get(
    'monitoring?sort=running%20desc&sort=created_at%20desc'
  );
  return data;
};

export const getMonitor = async (monitorId) => {
  const { data } = await $authHost.get(`monitoring/${monitorId}`);
  return data;
};

export const updateMonitor = async (monitorId, partialMonitorData) => {
  const { data } = await $authHost.patch(
    `monitoring/${monitorId}`,
    partialMonitorData
  );
  return data;
};

export const deleteMonitor = async (monitorId) => {
  const { data } = await $authHost.delete(`monitoring/${monitorId}`);
  return data;
};

export const getMonitorRequests = async (monitorId, params) => {
  const searchParams = new URLSearchParams(params);
  const { data } = await $authHost.get(
    `monitoring/${monitorId}/requests?${searchParams.toString()}`
  );
  return data;
};

export const postMonitor = async (monitorData) => {
  const { data } = await $authHost.post('monitoring', monitorData);
  return data;
};

export const getEvents = async (params) => {
  const searchParams = new URLSearchParams(params);
  const { data } = await $authHost.get(
    `monitoring/events?${searchParams.toString()}`
  );
  return data;
};
