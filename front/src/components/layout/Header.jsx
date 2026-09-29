import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";
import { colors, display } from "../../theme/tokens.js";
import { diamond } from "../../theme/styles.js";

export default function Header({ children }) {
  return (
    <Box
      component="header"
      sx={{
        bgcolor: colors.ink,
        px: { xs: 2, sm: "36px" },
        py: "22px",
        display: "flex",
        alignItems: "center",
        justifyContent: "space-between",
        gap: 2,
      }}
    >
      <Typography
        sx={{
          fontFamily: display,
          fontSize: 32,
          letterSpacing: "0.03em",
          color: colors.yellow,
          display: "flex",
          alignItems: "center",
          gap: "10px",
          "&::before": diamond(14, 3),
        }}
      >
        TaxiTech
      </Typography>
      <Box sx={{ display: "flex", alignItems: "center", gap: 2 }}>
        <Typography
          sx={{
            color: colors.bg,
            fontSize: 11,
            letterSpacing: "0.15em",
            textTransform: "uppercase",
            opacity: 0.6,
            display: { xs: "none", sm: "block" },
          }}
        >
          Digital Taximeter
        </Typography>
        {children}
      </Box>
    </Box>
  );
}
