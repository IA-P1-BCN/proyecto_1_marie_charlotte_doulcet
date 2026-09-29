import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it, vi } from "vitest";
import RideControls from "../../components/ride/RideControls.jsx";

const setup = (props = {}) => {
  const handlers = { onChangeState: vi.fn(), onEnd: vi.fn() };
  render(<RideControls state="stopped" pending={false} {...handlers} {...props} />);
  return handlers;
};

describe("RideControls", () => {
  it("requests the chosen state", async () => {
    const { onChangeState } = setup();
    await userEvent.click(screen.getByRole("button", { name: "Movimiento" }));
    expect(onChangeState).toHaveBeenCalledWith("moving");
  });

  it("marks the current state as pressed", () => {
    setup({ state: "moving" });
    expect(screen.getByRole("button", { name: "Movimiento" })).toHaveAttribute("aria-pressed", "true");
    expect(screen.getByRole("button", { name: "Parado" })).toHaveAttribute("aria-pressed", "false");
  });

  it("only ends the ride after confirming in the dialog", async () => {
    const { onEnd } = setup();
    await userEvent.click(screen.getByRole("button", { name: "Fin de carrera" }));
    expect(onEnd).not.toHaveBeenCalled();
    await userEvent.click(screen.getByRole("button", { name: "Finalizar" }));
    expect(onEnd).toHaveBeenCalledOnce();
  });

  it("disables the buttons while an action is pending", () => {
    setup({ pending: true });
    expect(screen.getByRole("button", { name: "Parado" })).toBeDisabled();
  });
});
