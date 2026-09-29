import { useEffect, useState } from "react";
import Table from "@mui/material/Table";
import TableHead from "@mui/material/TableHead";
import TableBody from "@mui/material/TableBody";
import TableRow from "@mui/material/TableRow";
import TableCell from "@mui/material/TableCell";
import Paper from "@mui/material/Paper";
import Typography from "@mui/material/Typography";
import CircularProgress from "@mui/material/CircularProgress";
import Alert from "@mui/material/Alert";
import Dialog from "@mui/material/Dialog";
import DialogTitle from "@mui/material/DialogTitle";
import DialogContent from "@mui/material/DialogContent";
import DialogActions from "@mui/material/DialogActions";
import Button from "@mui/material/Button";
import { colors } from "../theme.js";
import client from "../api/client.js";
import { formatDuration, formatDateTime } from "../format.js";

// Today's rides, newest first. `limit` caps the list; `reloadKey` forces a refetch.
export default function RideHistory({ limit, reloadKey = 0 }) {
  const [rides, setRides] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);
  const [selected, setSelected] = useState(null);

  useEffect(() => {
    client
      .get("/rides")
      .then(({ data }) => {
        const newestFirst = [...data].sort((a, b) => b.started_at.localeCompare(a.started_at));
        setRides(limit ? newestFirst.slice(0, limit) : newestFirst);
        setError(false);
      })
      .catch(() => setError(true))
      .finally(() => setLoading(false));
  }, [limit, reloadKey]);

  if (loading) {
    return (
      <Typography sx={{ textAlign: "center" }}>
        <CircularProgress />
      </Typography>
    );
  }

  if (error) {
    return <Alert severity="error">No se pudo cargar el historial. Inténtalo de nuevo.</Alert>;
  }

  if (rides.length === 0) {
    return <Typography>No hay carreras registradas hoy.</Typography>;
  }

  return (
    <Paper sx={{ overflow: "hidden" }}>
      <Table>
        <TableHead>
          <TableRow sx={{ bgcolor: colors.ink }}>
            <TableCell sx={{ color: colors.yellow }}>Fecha</TableCell>
            <TableCell sx={{ color: colors.yellow }}>Duración</TableCell>
            <TableCell sx={{ color: colors.yellow }} align="right">
              Importe
            </TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {rides.map((ride) => (
            <TableRow key={ride.id} hover onClick={() => setSelected(ride)} sx={{ cursor: "pointer" }}>
              <TableCell>{formatDateTime(ride.started_at)}</TableCell>
              <TableCell>{formatDuration(ride.duration_seconds)}</TableCell>
              <TableCell align="right" sx={{ color: colors.pinkText, fontWeight: 600 }}>
                {ride.amount.toFixed(2)}€
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
      <Dialog open={Boolean(selected)} onClose={() => setSelected(null)}>
        {selected && (
          <>
            <DialogTitle>Carrera #{selected.id}</DialogTitle>
            <DialogContent>
              <Typography>Inicio: {formatDateTime(selected.started_at)}</Typography>
              <Typography>Fin: {formatDateTime(selected.ended_at)}</Typography>
              <Typography>Duración: {formatDuration(selected.duration_seconds)}</Typography>
              <Typography sx={{ color: colors.pinkText, fontWeight: 600 }}>
                Importe: {selected.amount.toFixed(2)} €
              </Typography>
            </DialogContent>
            <DialogActions>
              <Button onClick={() => setSelected(null)}>Cerrar</Button>
            </DialogActions>
          </>
        )}
      </Dialog>
    </Paper>
  );
}
