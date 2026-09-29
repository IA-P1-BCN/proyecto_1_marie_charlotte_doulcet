import { act, renderHook } from "@testing-library/react";
import { afterEach, describe, expect, it } from "vitest";
import { AuthProvider } from "../../context/AuthContext.jsx";
import { useAuth } from "../../hooks/useAuth.js";
import { AUTH_EXPIRED, getToken } from "../../services/tokenStorage.js";

afterEach(() => localStorage.clear());

const setup = () => renderHook(() => useAuth(), { wrapper: AuthProvider });

describe("AuthContext", () => {
  it("starts logged out", () => {
    expect(setup().result.current.isAuthenticated).toBe(false);
  });

  it("login stores the token, logout clears it", () => {
    const { result } = setup();
    act(() => result.current.login("abc"));
    expect(result.current.isAuthenticated).toBe(true);
    expect(getToken()).toBe("abc");
    act(() => result.current.logout());
    expect(result.current.isAuthenticated).toBe(false);
    expect(getToken()).toBeNull();
  });

  it("logs out when the API announces the token expired", () => {
    const { result } = setup();
    act(() => result.current.login("abc"));
    act(() => {
      window.dispatchEvent(new Event(AUTH_EXPIRED));
    });
    expect(result.current.isAuthenticated).toBe(false);
  });
});
