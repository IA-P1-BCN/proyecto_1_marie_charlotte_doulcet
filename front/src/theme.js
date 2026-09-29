import { createTheme } from "@mui/material/styles";

// Tokens and component styles from docs/mockups/web-panel.html (Phase 4 "neon-checker pop"), followed to the letter.
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
  muted: "#5E5A55", // mockup uses ink@60% opacity for secondary text; solid value keeps it AA
};

export const display = "'Bebas Neue', sans-serif";

const check = "rgba(25,21,16,0.045)";
const offset = (px) => `${px}px ${px}px 0 ${colors.ink}`;

// Reusable pieces (mockup .panel / .btn / .section-title / .history-card).
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
export const btnMoving = { bgcolor: colors.yellow, color: colors.ink, boxShadow: offset(4), "&:hover": { bgcolor: colors.yellow, filter: "brightness(0.95)" } };
export const btnEnd = { bgcolor: colors.pinkText, color: "white", boxShadow: offset(4), "&:hover": { bgcolor: colors.pinkText, filter: "brightness(0.95)" } };
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

const theme = createTheme({
  palette: {
    background: { default: colors.bg, paper: colors.surface },
    text: { primary: colors.ink },
    primary: { main: colors.ink },
    secondary: { main: colors.pinkText },
  },
  typography: { fontFamily: "'DM Mono', monospace" },
  components: {
    MuiCssBaseline: {
      styleOverrides: {
        body: {
          backgroundColor: colors.bg,
          backgroundImage: [
            `linear-gradient(45deg, ${check} 25%, transparent 25%)`,
            `linear-gradient(-45deg, ${check} 25%, transparent 25%)`,
            `linear-gradient(45deg, transparent 75%, ${check} 75%)`,
            `linear-gradient(-45deg, transparent 75%, ${check} 75%)`,
          ].join(","),
          backgroundSize: "24px 24px",
          backgroundPosition: "0 0, 0 12px, 12px -12px, -12px 0px",
          minHeight: "100vh",
        },
      },
    },
    MuiButton: {
      styleOverrides: {
        root: {
          border: `3px solid ${colors.ink}`,
          borderRadius: 12,
          padding: 16,
          fontFamily: display,
          fontSize: 18,
          letterSpacing: "0.03em",
          textTransform: "none",
          lineHeight: "normal",
          color: colors.ink,
          backgroundColor: colors.surface,
          "&:hover": { backgroundColor: colors.surface, filter: "brightness(0.95)" },
          "&.Mui-disabled": { opacity: 0.55, color: colors.ink },
        },
      },
    },
    MuiDialog: {
      styleOverrides: {
        paper: { border: `4px solid ${colors.ink}`, borderRadius: 20, boxShadow: offset(10), backgroundImage: "none" },
      },
    },
    MuiDialogTitle: { styleOverrides: { root: { fontFamily: display, fontSize: 26, letterSpacing: "0.02em" } } },
    MuiDialogActions: { styleOverrides: { root: { padding: "8px 24px 24px", gap: 8 } } },
    MuiOutlinedInput: {
      styleOverrides: {
        root: {
          borderRadius: 12,
          backgroundColor: colors.surface,
          "& .MuiOutlinedInput-notchedOutline": { borderWidth: 3, borderColor: colors.ink },
          "&:hover .MuiOutlinedInput-notchedOutline": { borderColor: colors.ink },
          "&.Mui-focused .MuiOutlinedInput-notchedOutline": { borderWidth: 3, borderColor: colors.pinkText },
        },
      },
    },
    MuiInputLabel: { styleOverrides: { root: { color: colors.muted, "&.Mui-focused": { color: colors.pinkText } } } },
    MuiTableCell: { styleOverrides: { root: { borderBottom: `2px solid ${colors.bg}` } } },
  },
});

export default theme;
