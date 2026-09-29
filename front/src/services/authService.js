import client from "./apiClient.js";

export const getAuthStatus = () => client.get("/auth/status").then(({ data }) => data.registered);
export const login = (credentials) => client.post("/auth/login", credentials).then(({ data }) => data.token);
export const register = (credentials) => client.post("/auth/setup", credentials).then(({ data }) => data.token);
