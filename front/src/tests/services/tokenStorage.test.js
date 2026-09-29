import { afterEach, describe, expect, it, vi } from "vitest";
import { clearToken, getToken, setToken } from "../../services/tokenStorage.js";

afterEach(() => {
  vi.restoreAllMocks();
  localStorage.clear();
});

describe("tokenStorage", () => {
  it("stores, reads and clears the token", () => {
    setToken("abc");
    expect(getToken()).toBe("abc");
    clearToken();
    expect(getToken()).toBeNull();
  });

  it("never throws when storage is unavailable", () => {
    vi.spyOn(Storage.prototype, "getItem").mockImplementation(() => {
      throw new Error("blocked");
    });
    vi.spyOn(Storage.prototype, "setItem").mockImplementation(() => {
      throw new Error("blocked");
    });
    vi.spyOn(Storage.prototype, "removeItem").mockImplementation(() => {
      throw new Error("blocked");
    });
    expect(getToken()).toBeNull();
    expect(() => setToken("x")).not.toThrow();
    expect(() => clearToken()).not.toThrow();
  });
});
