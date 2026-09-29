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
import { colors } from "../theme.js";
import client from "../api/client.js";

function formatDuration(seconds) {
  const total = Math.round(seconds);
  const h = String(Math.floor(total / 3600)).padStart(2, "0");
  const m = String(Math.floor((total % 3600) / 60)).padStart(2, "0");
  const s = String(total % 60).padStart(2, "0");
  return `${h}:${m}:${s}`;
}

export default function RideHistory() {
  const [rides, setRides] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);

  useEffect(() => {
    client
      .get("/rides")
      .then(({ data }) => setRides(data))
      .catch(() => setError(true))
      .finally(() => setLoading(false));
  }, []);

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
            <TableRow key={ride.id}>
              <TableCell>{ride.started_at.replace("T", " ").slice(0, 16)}</TableCell>
              <TableCell>{formatDuration(ride.duration_seconds)}</TableCell>
              <TableCell align="right" sx={{ color: colors.pinkText, fontWeight: 600 }}>
                {ride.amount.toFixed(2)}€
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </Paper>
  );
}
