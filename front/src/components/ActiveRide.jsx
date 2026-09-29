import { useEffect, useState, useCallback } from "react";
import Box from "@mui/material/Box";
import Chip from "@mui/material/Chip";
import Typography from "@mui/material/Typography";
import Button from "@mui/material/Button";
import Dialog from "@mui/material/Dialog";
import DialogTitle from "@mui/material/DialogTitle";
import DialogActions from "@mui/material/DialogActions";
import Paper from "@mui/material/Paper";
import CircularProgress from "@mui/material/CircularProgress";
import { colors } from "../theme.js";
import client from "../api/client.js";
import { formatDuration } from "../format.js";
import RideHistory from "./RideHistory.jsx";
import StartRideDialog from "./StartRideDialog.jsx";

const REFRESH_MS = 1000;
const GENERIC_ERROR = "Error de conexión. Inténtalo de nuevo.";

export default function ActiveRide() {
  const [ride, setRide] = useState(null);
  const [loading, setLoading] = useState(true);
  const [pending, setPending] = useState(false);
  const [message, setMessage] = useState("");
  const [confirmEnd, setConfirmEnd] = useState(false);
  const [startOpen, setStartOpen] = useState(false);
  const [endedCount, setEndedCount] = useState(0);

  const fetchRide = useCallback(async () => {
    try {
      const { data } = await client.get("/ride");
      setRide(data);
      setMessage("");
    } catch (err) {
      if (err.response?.status === 404) {
        setRide(null);
      } else {
        setMessage("Sin conexión con el servidor.");
      }
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchRide();
    // ponytail: a stale poll response can land after a start/state/end action and
    // overwrite it for up to REFRESH_MS. Add a request counter if that flicker matters.
    const id = setInterval(fetchRide, REFRESH_MS);
    return () => clearInterval(id);
  }, [fetchRide]);

  const onStart = async (rates) => {
    setPending(true);
    try {
      const { data } = await client.post("/ride/start", rates);
      setRide(data);
      setMessage("");
    } catch (err) {
      setMessage(err.response?.status === 409 ? "Ya hay una carrera en curso." : GENERIC_ERROR);
    } finally {
      setPending(false);
    }
  };

  const onChangeState = async (state) => {
    setPending(true);
    try {
      const { data } = await client.patch("/ride/state", { state });
      setRide(data);
      setMessage("");
    } catch (err) {
      const status = err.response?.status;
      setMessage(
        status === 409 ? "Ya estás en ese estado." : status === 404 ? "No hay una carrera en curso." : GENERIC_ERROR,
      );
    } finally {
      setPending(false);
    }
  };

  const onEnd = async () => {
    setConfirmEnd(false);
    setPending(true);
    try {
      await client.post("/ride/end");
      setRide(null);
      setEndedCount((n) => n + 1);
      setMessage("Carrera finalizada.");
    } catch (err) {
      setMessage(err.response?.status === 404 ? "No hay una carrera en curso." : GENERIC_ERROR);
    } finally {
      setPending(false);
    }
  };

  if (loading) {
    return (
      <Paper sx={{ p: 4, textAlign: "center" }}>
        <CircularProgress />
      </Paper>
    );
  }

  const isMoving = ride?.state === "moving";

  const card = !ride ? (
      <Paper sx={{ p: 4, textAlign: "center" }}>
        <Typography sx={{ mb: 2 }}>Sin carrera activa.</Typography>
        <Button
          variant="contained"
          onClick={() => setStartOpen(true)}
          disabled={pending}
          sx={{ bgcolor: colors.yellow, color: colors.ink, "&:hover": { bgcolor: colors.yellow, filter: "brightness(0.92)" } }}
        >
          Iniciar carrera
        </Button>
        {message && (
          <Typography role="status" sx={{ mt: 2 }}>
            {message}
          </Typography>
        )}
      </Paper>
  ) : (
    <Paper sx={{ p: 4 }}>
      <Chip
        label={isMoving ? "En movimiento" : "Parado"}
        sx={{ bgcolor: isMoving ? colors.green : colors.pinkText, color: "white", mb: 2 }}
      />
      <Typography sx={{ fontFamily: "'Bebas Neue', sans-serif", fontSize: 64, color: colors.pinkText }}>
        {ride.amount_so_far.toFixed(2)} €
      </Typography>
      <Typography>{formatDuration(ride.elapsed_seconds)}</Typography>
      <Typography>{ride.current_rate} €/s</Typography>
      <Box sx={{ display: "flex", gap: 1, mt: 2, flexWrap: "wrap" }}>
        <Button variant="outlined" onClick={() => onChangeState("stopped")} disabled={pending} aria-pressed={!isMoving}>
          Parado
        </Button>
        <Button
          variant="contained"
          onClick={() => onChangeState("moving")}
          disabled={pending}
          aria-pressed={isMoving}
          sx={{ bgcolor: colors.yellow, color: colors.ink, "&:hover": { bgcolor: colors.yellow, filter: "brightness(0.92)" } }}
        >
          Movimiento
        </Button>
        <Button variant="contained" onClick={() => setConfirmEnd(true)} disabled={pending} sx={{ bgcolor: colors.pinkText }}>
          Fin de carrera
        </Button>
      </Box>
      {message && (
        <Typography role="status" sx={{ mt: 2 }}>
          {message}
        </Typography>
      )}
      <Dialog open={confirmEnd} onClose={() => setConfirmEnd(false)}>
        <DialogTitle>¿Finalizar la carrera actual?</DialogTitle>
        <DialogActions>
          <Button onClick={() => setConfirmEnd(false)}>Cancelar</Button>
          <Button variant="contained" onClick={onEnd} sx={{ bgcolor: colors.pinkText }}>
            Finalizar
          </Button>
        </DialogActions>
      </Dialog>
    </Paper>
  );

  return (
    <>
      {card}
      <Typography variant="h6" sx={{ mt: 4, mb: 1 }}>
        Historial de hoy
      </Typography>
      <RideHistory limit={10} reloadKey={endedCount} />
      <StartRideDialog open={startOpen} onClose={() => setStartOpen(false)} onStart={onStart} />
    </>
  );
}
