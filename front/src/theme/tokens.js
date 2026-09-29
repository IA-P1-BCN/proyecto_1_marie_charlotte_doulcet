// Design tokens from docs/mockups/web-panel.html ("neon-checker pop").
// pink (#FF4D6D) is large/decorative only (fails AA at normal text size);
// pinkText (#D6294B) is the text/fill-safe value — see DESIGN.md contrast table.
export const colors = {
  ink: "#191510",
  yellow: "#FFC629",
  bg: "#FFF9E8",
  surface: "#FFFFFF",
  pink: "#FF4D6D",
  pinkText: "#D6294B",
  green: "#0D7A56",
  tabInactive: "#5C4A12",
  muted: "#5E5A55", // mockup uses ink@60% opacity for secondary text; solid value keeps it AA
};

export const display = "'Bebas Neue', sans-serif";

export const offset = (px) => `${px}px ${px}px 0 ${colors.ink}`;
