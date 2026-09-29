import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";
import NoRidePanel from "./NoRidePanel.jsx";
import RideControls from "./RideControls.jsx";
import RideMeter from "./RideMeter.jsx";
import StateBadge from "./StateBadge.jsx";
import { panelSx } from "../../theme/styles.js";

export default function ActiveRidePanel({ ride, pending, message, onStart, onChangeState, onEnd }) {
  if (!ride) return <NoRidePanel pending={pending} message={message} onStart={onStart} />;

  return (
    <Box sx={panelSx}>
      <StateBadge state={ride.state} />
      <RideMeter ride={ride} />
      <RideControls state={ride.state} pending={pending} onChangeState={onChangeState} onEnd={onEnd} />
      {message && (
        <Typography role="status" sx={{ mt: 2 }}>
          {message}
        </Typography>
      )}
    </Box>
  );
}
