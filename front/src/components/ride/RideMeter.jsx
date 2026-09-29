import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";
import { colors, display } from "../../theme/tokens.js";
import { formatDuration } from "../../utils/format.js";

// Live fare, elapsed time and current rate.
export default function RideMeter({ ride }) {
  return (
    <>
      <Box sx={{ display: "flex", alignItems: "baseline", gap: "4px", mb: "4px" }}>
        <Box component="span" sx={{ fontFamily: display, fontSize: 40, color: colors.pink }}>
          €
        </Box>
        <Box component="span" sx={{ fontFamily: display, fontSize: 96, lineHeight: 0.9, color: colors.ink }}>
          {ride.amount_so_far.toFixed(2)}
        </Box>
      </Box>
      <Typography sx={{ fontSize: 13, color: colors.muted, mb: "28px" }}>
        {`${formatDuration(ride.elapsed_seconds)} transcurrido · tarifa ${ride.current_rate}€/s`}
      </Typography>
    </>
  );
}
