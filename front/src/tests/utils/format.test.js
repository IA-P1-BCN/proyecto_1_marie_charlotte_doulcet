import { describe, expect, it } from "vitest";
import { formatDateTime, formatDuration } from "../../utils/format.js";

describe("format", () => {
  it("formats seconds as HH:MM:SS", () => {
    expect(formatDuration(0)).toBe("00:00:00");
    expect(formatDuration(872)).toBe("00:14:32");
    expect(formatDuration(3661.4)).toBe("01:01:01");
  });

  it("formats an ISO datetime to minutes", () => {
    expect(formatDateTime("2026-09-17T00:14:32")).toBe("2026-09-17 00:14");
  });
});
