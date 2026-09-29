import { render, screen, waitFor, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { MemoryRouter } from "react-router-dom";
import { describe, it, expect, vi, beforeEach } from "vitest";
import App from "./App.jsx";
import client from "./api/client.js";

vi.mock("./api/client.js", () => ({
  default: { get: vi.fn(), post: vi.fn(), patch: vi.fn(), put: vi.fn() },
}));

function renderAt(path) {
  return render(
    <MemoryRouter initialEntries={[path]}>
      <App />
    </MemoryRouter>,
  );
}

const activeRide = {
  state: "stopped",
  started_at: "2026-09-17T00:14:00",
  amount_so_far: 1.5,
  elapsed_seconds: 75,
  current_rate: 0.02,
};
const ride = {
  id: 1,
  started_at: "2026-09-17T00:14:00",
  ended_at: "2026-09-17T00:28:32",
  duration_seconds: 872,
  amount: 12.4,
};

// Routes GET by url so component fetch order doesn't matter.
function mockGet({ active = activeRide, rides = [ride], passwordSet = true } = {}) {
  client.get.mockImplementation((url) => {
    if (url === "/auth/status") return Promise.resolve({ data: { password_set: passwordSet } });
    if (url === "/ride") return active ? Promise.resolve({ data: active }) : Promise.reject({ response: { status: 404 } });
    if (url === "/rides") return Promise.resolve({ data: rides });
    if (url === "/rates") return Promise.resolve({ data: { stopped_rate: 0.02, moving_rate: 0.05 } });
  });
}

beforeEach(() => {
  vi.clearAllMocks();
  localStorage.setItem("token", "t"); // logged in by default
});

describe("App", () => {
  it("renders state, fare, elapsed time and current rate", async () => {
    mockGet({ active: { ...activeRide, state: "moving", amount_so_far: 12.4, current_rate: 0.05 } });
    renderAt("/");

    expect(await screen.findByText("En movimiento")).toBeInTheDocument();
    expect(screen.getByText("12.40 €")).toBeInTheDocument();
    expect(screen.getByText("00:01:15")).toBeInTheDocument();
    expect(screen.getByText("0.05 €/s")).toBeInTheDocument();
  });

  it("shows today's history under the active ride and opens a ride's detail on click", async () => {
    mockGet();
    renderAt("/");

    await userEvent.click(await screen.findByText("12.40€"));
    const dialog = await screen.findByRole("dialog");
    expect(within(dialog).getByText(/00:14:32/)).toBeInTheDocument();
  });

  it("shows only the 10 most recent rides on the active screen", async () => {
    const rides = Array.from({ length: 12 }, (_, i) => ({
      ...ride,
      id: i + 1,
      started_at: `2026-09-17T10:${String(i).padStart(2, "0")}:00`,
      amount: i + 1,
    }));
    mockGet({ rides });
    renderAt("/");

    await screen.findByText("12.00€");
    expect(screen.queryByText("1.00€")).not.toBeInTheDocument();
    expect(screen.queryByText("2.00€")).not.toBeInTheDocument();
    expect(screen.getByText("3.00€")).toBeInTheDocument();
  });

  it("renders the full history page", async () => {
    mockGet();
    renderAt("/historial");
    expect(await screen.findByText("12.40€")).toBeInTheDocument();
  });

  it("shows empty-state message when history is []", async () => {
    mockGet({ rides: [] });
    renderAt("/historial");
    await waitFor(() => {
      expect(screen.getByText("No hay carreras registradas hoy.")).toBeInTheDocument();
    });
  });

  it("starts a ride with the rates chosen in the pre-ride dialog", async () => {
    mockGet({ active: null });
    client.post.mockResolvedValueOnce({ data: activeRide });
    renderAt("/");

    await userEvent.click(await screen.findByRole("button", { name: "Iniciar carrera" }));
    const dialog = await screen.findByRole("dialog");
    const stopped = await within(dialog).findByLabelText("Parado (€/s)");
    await waitFor(() => expect(stopped).toHaveValue(0.02));
    await userEvent.clear(stopped);
    await userEvent.type(stopped, "0.03");
    await userEvent.click(within(dialog).getByRole("button", { name: "Empezar carrera" }));

    await waitFor(() =>
      expect(client.post).toHaveBeenCalledWith("/ride/start", { stopped_rate: 0.03, moving_rate: 0.05 }),
    );
    expect(client.put).not.toHaveBeenCalled();
  });

  it("saves the rates as defaults when the checkbox is ticked", async () => {
    mockGet({ active: null });
    client.post.mockResolvedValueOnce({ data: activeRide });
    client.put.mockResolvedValueOnce({ data: {} });
    renderAt("/");

    await userEvent.click(await screen.findByRole("button", { name: "Iniciar carrera" }));
    const dialog = await screen.findByRole("dialog");
    await waitFor(() => expect(within(dialog).getByLabelText("Parado (€/s)")).toHaveValue(0.02));
    await userEvent.click(within(dialog).getByLabelText("Guardar como tarifas por defecto"));
    await userEvent.click(within(dialog).getByRole("button", { name: "Empezar carrera" }));

    await waitFor(() =>
      expect(client.put).toHaveBeenCalledWith("/rates", { stopped_rate: 0.02, moving_rate: 0.05 }),
    );
  });

  it("rejects non-positive rates without starting the ride", async () => {
    mockGet({ active: null });
    renderAt("/");

    await userEvent.click(await screen.findByRole("button", { name: "Iniciar carrera" }));
    const dialog = await screen.findByRole("dialog");
    const moving = await within(dialog).findByLabelText("Movimiento (€/s)");
    await waitFor(() => expect(moving).toHaveValue(0.05));
    await userEvent.clear(moving);
    await userEvent.type(moving, "0");
    await userEvent.click(within(dialog).getByRole("button", { name: "Empezar carrera" }));

    expect(within(dialog).getByText("Las tarifas deben ser números positivos.")).toBeInTheDocument();
    expect(client.post).not.toHaveBeenCalled();
  });

  it("shows a message when the requested state is already the current one", async () => {
    mockGet();
    client.patch.mockRejectedValueOnce({ response: { status: 409 } });
    renderAt("/");

    await userEvent.click(await screen.findByRole("button", { name: "Parado" }));
    expect(await screen.findByRole("status")).toHaveTextContent("Ya estás en ese estado.");
  });

  it("confirms with an in-app dialog, then returns to the start screen", async () => {
    mockGet();
    client.post.mockResolvedValueOnce({ data: {} });
    renderAt("/");

    await userEvent.click(await screen.findByRole("button", { name: "Fin de carrera" }));
    const dialog = await screen.findByRole("dialog");
    mockGet({ active: null });
    await userEvent.click(within(dialog).getByRole("button", { name: "Finalizar" }));

    expect(await screen.findByRole("button", { name: "Iniciar carrera" })).toBeInTheDocument();
    expect(screen.getByRole("status")).toHaveTextContent("Carrera finalizada.");
  });

  describe("auth", () => {
    beforeEach(() => localStorage.removeItem("token"));

    it("asks for the password when logged out, then shows the app", async () => {
      mockGet();
      client.post.mockResolvedValueOnce({ data: { token: "abc" } });
      renderAt("/");

      await userEvent.type(await screen.findByLabelText("Contraseña"), "secreto123");
      await userEvent.click(screen.getByRole("button", { name: "Entrar" }));

      expect(client.post).toHaveBeenCalledWith("/auth/login", { password: "secreto123" });
      expect(await screen.findByRole("button", { name: "Cerrar sesión" })).toBeInTheDocument();
      expect(localStorage.getItem("token")).toBe("abc");
    });

    it("shows an error on a wrong password", async () => {
      mockGet();
      client.post.mockRejectedValueOnce({ response: { status: 401 } });
      renderAt("/");

      await userEvent.type(await screen.findByLabelText("Contraseña"), "mala");
      await userEvent.click(screen.getByRole("button", { name: "Entrar" }));

      expect(await screen.findByRole("alert")).toHaveTextContent("Contraseña incorrecta.");
    });

    it("offers to create the password on first use and checks the confirmation", async () => {
      mockGet({ passwordSet: false });
      client.post.mockResolvedValueOnce({ data: { token: "abc" } });
      renderAt("/");

      await userEvent.type(await screen.findByLabelText("Contraseña"), "secreto123");
      await userEvent.type(screen.getByLabelText("Confirmar contraseña"), "distinta");
      await userEvent.click(screen.getByRole("button", { name: "Crear contraseña" }));
      expect(await screen.findByRole("alert")).toHaveTextContent("Las contraseñas no coinciden.");
      expect(client.post).not.toHaveBeenCalled();

      await userEvent.clear(screen.getByLabelText("Confirmar contraseña"));
      await userEvent.type(screen.getByLabelText("Confirmar contraseña"), "secreto123");
      await userEvent.click(screen.getByRole("button", { name: "Crear contraseña" }));
      expect(client.post).toHaveBeenCalledWith("/auth/setup", { password: "secreto123" });
    });
  });

  it("logs out from the app bar", async () => {
    mockGet();
    renderAt("/");

    await userEvent.click(await screen.findByRole("button", { name: "Cerrar sesión" }));

    expect(await screen.findByLabelText("Contraseña")).toBeInTheDocument();
    expect(localStorage.getItem("token")).toBeNull();
  });
});
