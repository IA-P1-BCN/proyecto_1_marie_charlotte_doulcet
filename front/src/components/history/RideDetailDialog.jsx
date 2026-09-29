import Button from "@mui/material/Button";
import Dialog from "@mui/material/Dialog";
import DialogActions from "@mui/material/DialogActions";
import DialogContent from "@mui/material/DialogContent";
import DialogTitle from "@mui/material/DialogTitle";
import Typography from "@mui/material/Typography";
import { colors } from "../../theme/tokens.js";
import { formatDateTime, formatDuration } from "../../utils/format.js";

export default function RideDetailDialog({ ride, onClose }) {
  return (
    <Dialog open={Boolean(ride)} onClose={onClose}>
      {ride && (
        <>
          <DialogTitle>Carrera #{ride.id}</DialogTitle>
          <DialogContent>
            <Typography>Inicio: {formatDateTime(ride.started_at)}</Typography>
            <Typography>Fin: {formatDateTime(ride.ended_at)}</Typography>
            <Typography>Duración: {formatDuration(ride.duration_seconds)}</Typography>
            <Typography sx={{ color: colors.pinkText, fontWeight: 600 }}>Importe: {ride.amount.toFixed(2)} €</Typography>
          </DialogContent>
          <DialogActions>
            <Button onClick={onClose}>Cerrar</Button>
          </DialogActions>
        </>
      )}
    </Dialog>
  );
}
