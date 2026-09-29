import { act, renderHook, waitFor } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";
import { useActiveRide } from "../../hooks/useActiveRide.js";
import { changeRideState, endRide, getActiveRide, startRide } from "../../services/rideService.js";

vi.mock("../../services/rideService.js", () => ({
  getActiveRide: vi.fn(),
  startRide: vi.fn(),
  changeRideState: vi.fn(),
  endRide: vi.fn(),
}));

const httpError = (status) => ({ response: { status } });
const ride = { state: "stopped", amount_so_far: 0 };

beforeEach(() => vi.clearAllMocks());

async function loaded() {
  const hook = renderHook(() => useActiveRide());
  await waitFor(() => expect(hook.result.current.loading).toBe(false));
  return hook;
}

describe("useActiveRide", () => {
  it("has no ride when the API answers 404", async () => {
    getActiveRide.mockRejectedValue(httpError(404));
    const { result } = await loaded();
    expect(result.current.ride).toBeNull();
    expect(result.current.message).toBe("");
  });

  it("reports a connection problem on other errors", async () => {
    getActiveRide.mockRejectedValue(httpError(500));
    const { result } = await loaded();
    expect(result.current.message).toBe("Sin conexión con el servidor.");
  });

  it("maps a 409 on state change to a friendly message", async () => {
    getActiveRide.mockResolvedValue(ride);
    changeRideState.mockRejectedValue(httpError(409));
    const { result } = await loaded();
    await act(() => result.current.changeState("stopped"));
    expect(result.current.message).toBe("Ya estás en ese estado.");
  });

  it("starts a ride and stores it", async () => {
    getActiveRide.mockRejectedValue(httpError(404));
    startRide.mockResolvedValue(ride);
    const { result } = await loaded();
    await act(() => result.current.start({ stopped_rate: 0.02, moving_rate: 0.05 }));
    expect(result.current.ride).toEqual(ride);
  });

  it("ends the ride, clears it and bumps endedCount so history reloads", async () => {
    getActiveRide.mockResolvedValue(ride);
    endRide.mockResolvedValue({});
    const { result } = await loaded();
    await act(() => result.current.end());
    expect(result.current.ride).toBeNull();
    expect(result.current.endedCount).toBe(1);
    expect(result.current.message).toBe("Carrera finalizada.");
  });
});
