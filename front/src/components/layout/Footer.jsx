import Typography from "@mui/material/Typography";
import { colors } from "../../theme/tokens.js";

export default function Footer() {
  return (
    <Typography
      component="footer"
      sx={{ textAlign: "center", p: 4, fontSize: 11, color: colors.muted, letterSpacing: "0.1em", textTransform: "uppercase" }}
    >
      TaxiTech Solutions · Digital Taximeter
    </Typography>
  );
}
