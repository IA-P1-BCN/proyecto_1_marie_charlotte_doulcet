// Session token lives in localStorage; wrapped because storage can throw (private mode, blocked site data).
const KEY = "token";

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
  } catch {
    /* session just won't survive a reload */
  }
};

export const clearToken = () => {
  try {
    localStorage.removeItem(KEY);
  } catch {
    /* nothing stored */
  }
};

export const AUTH_EXPIRED = "auth-expired";
