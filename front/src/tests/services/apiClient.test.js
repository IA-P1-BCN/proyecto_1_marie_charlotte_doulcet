import { afterEach, describe, expect, it, vi } from "vitest";
import client from "../../services/apiClient.js";
import { AUTH_EXPIRED, getToken, setToken } from "../../services/tokenStorage.js";

const rejectWith = (status, url) => ({ response: { status }, config: { url } });
const runRequest = (config = {}) => client.interceptors.request.handlers[0].fulfilled({ headers: {}, ...config });
const runError = (error) => client.interceptors.response.handlers[0].rejected(error);

afterEach(() => localStorage.clear());

describe("apiClient", () => {
  it("adds the Bearer token when logged in", () => {
    setToken("abc");
    expect(runRequest().headers.Authorization).toBe("Bearer abc");
  });

  it("sends no Authorization header when logged out", () => {
    expect(runRequest().headers.Authorization).toBeUndefined();
  });

  it("clears the token and announces expiry on a 401 outside /auth", async () => {
    setToken("abc");
    const listener = vi.fn();
    window.addEventListener(AUTH_EXPIRED, listener);
    await expect(runError(rejectWith(401, "/ride"))).rejects.toBeTruthy();
    window.removeEventListener(AUTH_EXPIRED, listener);
    expect(getToken()).toBeNull();
    expect(listener).toHaveBeenCalledOnce();
  });

  it("keeps the session on a 401 from the auth endpoints (wrong password)", async () => {
    setToken("abc");
    await expect(runError(rejectWith(401, "/auth/login"))).rejects.toBeTruthy();
    expect(getToken()).toBe("abc");
  });
});
