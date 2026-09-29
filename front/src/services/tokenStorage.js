const KEY = "token";

export const AUTH_EXPIRED = "auth-expired";

export const getToken = () => {
  try {
    return localStorage.getItem(KEY);
  } catch {
    return null;
  }
};

export const setToken = (token) => {
  try {
    localStorage.setItem(KEY, token);
  } catch {}
};

export const clearToken = () => {
  try {
    localStorage.removeItem(KEY);
  } catch {}
};
