import Typography from "@mui/material/Typography";
import { display } from "../../theme/tokens.js";
import { diamond } from "../../theme/styles.js";

export default function SectionTitle({ children }) {
  return (
    <Typography
      sx={{
        fontFamily: display,
        fontSize: 22,
        letterSpacing: "0.02em",
        mb: "18px",
        display: "flex",
        alignItems: "center",
        gap: "10px",
        "&::before": diamond(18, 4, true),
      }}
    >
      {children}
    </Typography>
  );
}
