import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || '/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const generateTask = async (username) => {
  const response = await api.post('/task/generate', { username });
  return response.data;
};

export const evaluateAnswer = async (taskId, answer) => {
  const response = await api.post('/task/evaluate', {
    task_id: taskId,
    answer: answer,
  });
  return response.data;
};

export const getUserStats = async (username) => {
  const response = await api.get(`/user/${username}/stats`);
  return response.data;
};

export default api;
