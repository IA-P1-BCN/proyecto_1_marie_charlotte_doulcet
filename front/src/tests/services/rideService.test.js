import { beforeEach, describe, expect, it, vi } from "vitest";
import client from "../../services/apiClient.js";
import { changeRideState, endRide, getActiveRide, getTodayRides, startRide } from "../../services/rideService.js";

vi.mock("../../services/apiClient.js", () => ({
  default: { get: vi.fn(), post: vi.fn(), patch: vi.fn(), put: vi.fn() },
}));

beforeEach(() => vi.clearAllMocks());

describe("rideService", () => {
  it("returns the response body, not the axios envelope", async () => {
    client.get.mockResolvedValue({ data: { state: "stopped" } });
    expect(await getActiveRide()).toEqual({ state: "stopped" });
    expect(client.get).toHaveBeenCalledWith("/ride");
  });

  it("starts a ride with the chosen rates", async () => {
    client.post.mockResolvedValue({ data: {} });
    await startRide({ stopped_rate: 0.03, moving_rate: 0.05 });
    expect(client.post).toHaveBeenCalledWith("/ride/start", { stopped_rate: 0.03, moving_rate: 0.05 });
  });

  it("changes the state", async () => {
    client.patch.mockResolvedValue({ data: {} });
    await changeRideState("moving");
    expect(client.patch).toHaveBeenCalledWith("/ride/state", { state: "moving" });
  });

  it("ends a ride and lists today's rides", async () => {
    client.post.mockResolvedValue({ data: { id: 1 } });
    client.get.mockResolvedValue({ data: [{ id: 1 }] });
    expect(await endRide()).toEqual({ id: 1 });
    expect(await getTodayRides()).toEqual([{ id: 1 }]);
    expect(client.get).toHaveBeenLastCalledWith("/rides");
  });
});
