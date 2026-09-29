import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import RideDetailDialog from "../../components/history/RideDetailDialog.jsx";

const ride = {
  id: 7,
  started_at: "2026-09-17T00:14:00",
  ended_at: "2026-09-17T00:28:32",
  duration_seconds: 872,
  amount: 12.4,
};

describe("RideDetailDialog", () => {
  it("shows nothing without a ride", () => {
    render(<RideDetailDialog ride={null} onClose={() => {}} />);
    expect(screen.queryByRole("dialog")).not.toBeInTheDocument();
  });

  it("shows the ride's details", () => {
    render(<RideDetailDialog ride={ride} onClose={() => {}} />);
    expect(screen.getByText("Carrera #7")).toBeInTheDocument();
    expect(screen.getByText(/00:14:32/)).toBeInTheDocument();
    expect(screen.getByText("Importe: 12.40 €")).toBeInTheDocument();
  });
});
