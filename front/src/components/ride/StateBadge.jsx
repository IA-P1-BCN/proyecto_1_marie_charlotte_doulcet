import Box from "@mui/material/Box";
import { colors } from "../../theme/tokens.js";
import { RIDE_STATE } from "../../utils/rideState.js";

export default function StateBadge({ state }) {
  const isMoving = state === RIDE_STATE.MOVING;
  return (
    <Box
      sx={{
        display: "inline-flex",
        alignItems: "center",
        gap: 1,
        bgcolor: isMoving ? colors.green : colors.pinkText,
        color: "white",
        px: 2,
        py: 1,
        borderRadius: 999,
        border: `2px solid ${colors.ink}`,
        fontSize: 12,
        letterSpacing: "0.08em",
        textTransform: "uppercase",
        fontWeight: 500,
        mb: "28px",
      }}
    >
      <Box
        sx={{
          width: 8,
          height: 8,
          borderRadius: "50%",
          bgcolor: "white",
          ...(isMoving && {
            animation: "pulse 1.5s infinite",
            "@keyframes pulse": {
              "0%": { boxShadow: "0 0 0 0 rgba(255,255,255,0.5)" },
              "70%": { boxShadow: "0 0 0 8px rgba(255,255,255,0)" },
              "100%": { boxShadow: "0 0 0 0 rgba(255,255,255,0)" },
            },
          }),
        }}
      />
      {isMoving ? "En movimiento" : "Parado"}
    </Box>
  );
}
