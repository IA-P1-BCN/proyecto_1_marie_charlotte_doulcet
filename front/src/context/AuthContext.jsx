import { createContext, useCallback, useEffect, useMemo, useState } from "react";
import { AUTH_EXPIRED, clearToken, getToken, setToken } from "../services/tokenStorage.js";

export const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [token, setTokenState] = useState(getToken);

  useEffect(() => {
    const expire = () => setTokenState(null);
    window.addEventListener(AUTH_EXPIRED, expire);
    return () => window.removeEventListener(AUTH_EXPIRED, expire);
  }, []);

  const login = useCallback((newToken) => {
    setToken(newToken);
    setTokenState(newToken);
  }, []);

  const logout = useCallback(() => {
    clearToken();
    setTokenState(null);
  }, []);

  const value = useMemo(() => ({ isAuthenticated: Boolean(token), login, logout }), [token, login, logout]);
  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}
