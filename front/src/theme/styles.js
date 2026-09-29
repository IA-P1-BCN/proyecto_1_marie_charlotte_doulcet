import { colors, offset } from "./tokens.js";

// Reusable sx fragments (mockup .panel / .btn / .section-title / .history-card).
export const panelSx = {
  bgcolor: colors.surface,
  border: `4px solid ${colors.ink}`,
  borderRadius: "20px",
  p: { xs: 3, sm: "36px" },
  boxShadow: offset(10),
  mb: 7,
};

export const cardSx = {
  bgcolor: colors.surface,
  border: `3px solid ${colors.ink}`,
  borderRadius: "16px",
  overflow: "hidden",
  boxShadow: "none",
};

export const btnMoving = {
  bgcolor: colors.yellow,
  color: colors.ink,
  boxShadow: offset(4),
  "&:hover": { bgcolor: colors.yellow, filter: "brightness(0.95)" },
};

export const btnEnd = {
  bgcolor: colors.pinkText,
  color: "white",
  boxShadow: offset(4),
  "&:hover": { bgcolor: colors.pinkText, filter: "brightness(0.95)" },
};

export const diamond = (size, radius, border = false) => ({
  content: '""',
  display: "inline-block",
  width: size,
  height: size,
  bgcolor: colors.pink,
  borderRadius: `${radius}px`,
  transform: "rotate(45deg)",
  ...(border && { border: `2px solid ${colors.ink}` }),
});
