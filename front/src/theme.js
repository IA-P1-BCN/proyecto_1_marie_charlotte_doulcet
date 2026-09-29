import { createTheme } from "@mui/material/styles";

// Tokens from docs/DESIGN.md — Phase 4 "neon-checker pop" web panel palette.
// pink (#FF4D6D) is large/decorative only (fails AA at normal text size);
// pink-text (#D6294B) is the text/fill-safe value — see DESIGN.md contrast table.
export const colors = {
  ink: "#191510",
  yellow: "#FFC629",
  bg: "#FFF9E8",
  surface: "#FFFFFF",
  pink: "#FF4D6D",
  pinkText: "#D6294B",
  green: "#0D7A56",
  tabInactive: "#5C4A12",
};

const theme = createTheme({
  palette: {
    background: { default: colors.bg, paper: colors.surface },
    text: { primary: colors.ink },
    primary: { main: colors.ink },
    secondary: { main: colors.pinkText },
  },
  typography: {
    fontFamily: "'DM Mono', monospace",
  },
});

export default theme;
