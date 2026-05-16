import axios from 'axios'

import {useAuthStore} from "@/stores/auth"

const http = axios.create({
  baseURL: 'http://localhost/api/v1/',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Интерцептор для добавления токена
http.interceptors.request.use((config) => {
  const authStore = useAuthStore();
  if (authStore.token) {
    config.headers.Authorization = `Bearer ${authStore.token}`;
  }
  return config;
});

// Интерцептор для обработки ошибок
http.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      console.log("status: " + error.response?.status)
      const authStore = useAuthStore();
      authStore.logout();
    }
    return Promise.reject(error);
  }
);

export default http;
