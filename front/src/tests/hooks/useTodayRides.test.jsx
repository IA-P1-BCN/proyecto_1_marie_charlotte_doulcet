import { renderHook, waitFor } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";
import { useTodayRides } from "../../hooks/useTodayRides.js";
import { getTodayRides } from "../../services/rideService.js";

vi.mock("../../services/rideService.js", () => ({ getTodayRides: vi.fn() }));

const ride = (id, hour) => ({ id, started_at: `2026-09-17T${hour}:00:00` });

beforeEach(() => vi.clearAllMocks());

describe("useTodayRides", () => {
  it("sorts newest first and applies the limit", async () => {
    getTodayRides.mockResolvedValue([ride(1, "08"), ride(2, "12"), ride(3, "10")]);
    const { result } = renderHook(() => useTodayRides({ limit: 2 }));
    await waitFor(() => expect(result.current.loading).toBe(false));
    expect(result.current.rides.map((r) => r.id)).toEqual([2, 3]);
  });

  it("flags an error when the request fails", async () => {
    getTodayRides.mockRejectedValue(new Error("down"));
    const { result } = renderHook(() => useTodayRides());
    await waitFor(() => expect(result.current.error).toBe(true));
    expect(result.current.rides).toEqual([]);
  });
});
