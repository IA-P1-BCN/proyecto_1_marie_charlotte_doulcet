import axios from "axios";
import { getToken, clearToken, AUTH_EXPIRED } from "../auth.js";

const client = axios.create({ baseURL: "/api" });

client.interceptors.request.use((config) => {
  const token = getToken();
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

// A 401 outside the auth endpoints means the token is gone (e.g. server restarted): back to login.
client.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401 && !error.config?.url?.startsWith("/auth/")) {
      clearToken();
      window.dispatchEvent(new Event(AUTH_EXPIRED));
    }
    return Promise.reject(error);
  },
);

export default client;
