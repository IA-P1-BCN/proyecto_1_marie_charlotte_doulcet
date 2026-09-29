import { useState } from "react";
import Box from "@mui/material/Box";
import Button from "@mui/material/Button";
import Typography from "@mui/material/Typography";
import StartRideDialog from "./StartRideDialog.jsx";
import { btnMoving, panelSx } from "../../theme/styles.js";

export default function NoRidePanel({ pending, message, onStart }) {
  const [startOpen, setStartOpen] = useState(false);
  return (
    <Box sx={{ ...panelSx, textAlign: "center" }}>
      <Typography sx={{ mb: 3 }}>Sin carrera activa.</Typography>
      <Button onClick={() => setStartOpen(true)} disabled={pending} sx={btnMoving}>
        Iniciar carrera
      </Button>
      {message && (
        <Typography role="status" sx={{ mt: 2 }}>
          {message}
        </Typography>
      )}
      <StartRideDialog open={startOpen} onClose={() => setStartOpen(false)} onStart={onStart} />
    </Box>
  );
}
