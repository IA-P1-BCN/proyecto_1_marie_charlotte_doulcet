import { render, screen, waitFor, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { MemoryRouter } from "react-router-dom";
import { describe, it, expect, vi, beforeEach } from "vitest";
import App from "./App.jsx";
import client from "./api/client.js";

vi.mock("./api/client.js", () => ({
  default: { get: vi.fn(), post: vi.fn(), patch: vi.fn() },
}));

function renderAt(path) {
  return render(
    <MemoryRouter initialEntries={[path]}>
      <App />
    </MemoryRouter>,
  );
}

beforeEach(() => {
  vi.clearAllMocks();
});

describe("App", () => {
  it("renders active ride state and fare from a mocked GET /api/ride", async () => {
    client.get.mockResolvedValueOnce({
      data: { state: "moving", started_at: "2026-09-17T00:14:00", amount_so_far: 12.4 },
    });

    renderAt("/");

    expect(await screen.findByText("En movimiento")).toBeInTheDocument();
    expect(screen.getByText("12.40 €")).toBeInTheDocument();
  });

  it("renders ride history rows from a mocked GET /api/rides", async () => {
    client.get.mockResolvedValueOnce({
      data: [
        {
          id: 1,
          started_at: "2026-09-17T00:14:00",
          ended_at: "2026-09-17T00:28:32",
          duration_seconds: 872,
          amount: 12.4,
        },
      ],
    });

    renderAt("/historial");

    expect(await screen.findByText("12.40€")).toBeInTheDocument();
    expect(screen.getByText("00:14:32")).toBeInTheDocument();
  });

  it("shows empty-state message when history is []", async () => {
    client.get.mockResolvedValueOnce({ data: [] });

    renderAt("/historial");

    await waitFor(() => {
      expect(screen.getByText("No hay carreras registradas hoy.")).toBeInTheDocument();
    });
  });

  const activeRide = { state: "stopped", started_at: "2026-09-17T00:14:00", amount_so_far: 1.5 };

  it("shows a message when the requested state is already the current one", async () => {
    client.get.mockResolvedValue({ data: activeRide });
    client.patch.mockRejectedValueOnce({ response: { status: 409 } });

    renderAt("/");
    await userEvent.click(await screen.findByRole("button", { name: "Parado" }));

    expect(await screen.findByRole("status")).toHaveTextContent("Ya estás en ese estado.");
  });

  it("confirms with an in-app dialog, then returns to the start screen", async () => {
    client.get.mockResolvedValue({ data: activeRide });
    client.post.mockResolvedValueOnce({ data: {} });

    renderAt("/");
    await userEvent.click(await screen.findByRole("button", { name: "Fin de carrera" }));
    const dialog = await screen.findByRole("dialog");
    await userEvent.click(within(dialog).getByRole("button", { name: "Finalizar" }));

    expect(await screen.findByRole("button", { name: "Iniciar carrera" })).toBeInTheDocument();
    expect(screen.getByRole("status")).toHaveTextContent("Carrera finalizada.");
  });
});
