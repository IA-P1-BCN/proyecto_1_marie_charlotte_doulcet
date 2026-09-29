import { createTheme } from "@mui/material/styles";
import { colors, display, offset } from "./tokens.js";

const check = "rgba(25,21,16,0.045)";

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
