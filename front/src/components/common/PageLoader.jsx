import Box from "@mui/material/Box";
import CircularProgress from "@mui/material/CircularProgress";
import { panelSx } from "../../theme/styles.js";

export default function PageLoader() {
  return (
    <Box sx={{ ...panelSx, textAlign: "center" }}>
      <CircularProgress />
    </Box>
  );
}
