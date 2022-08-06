import jwtDecode from 'jwt-decode';
import { $authHost, $host } from './index';

export const signup = async (username, password, passwordConfirmation) => {
  const { data } = await $host.post('auth/signup', {
    username,
    password,
    password_confirmation: passwordConfirmation,
  });

  if (data) {
    const token = data.content.access_token;
    localStorage.setItem('accessToken', token);
    return jwtDecode(token);
  }

  return null;
};

export const login = async (username, password) => {
  const { data } = await $host.post('auth/login', { username, password });

  const token = data.content.access_token;
  localStorage.setItem('accessToken', token);
  return jwtDecode(token);
};

export const check = async () => {
  const { data } = await $authHost.get('auth/check');

  if (data.content.auth) {
    return jwtDecode(data.content.access_token);
  }

  return null;
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
