import { useEffect, useState, useCallback } from "react";
import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";
import Button from "@mui/material/Button";
import Dialog from "@mui/material/Dialog";
import DialogTitle from "@mui/material/DialogTitle";
import DialogActions from "@mui/material/DialogActions";
import CircularProgress from "@mui/material/CircularProgress";
import { colors, display, panelSx, btnMoving, btnEnd, diamond } from "../theme.js";
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
      <Box sx={{ ...panelSx, textAlign: "center" }}>
        <CircularProgress />
      </Box>
    );
  }

  const isMoving = ride?.state === "moving";

  const card = !ride ? (
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
    </Box>
  ) : (
    <Box sx={panelSx}>
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
      <Box sx={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "12px" }}>
        <Button onClick={() => onChangeState("stopped")} disabled={pending} aria-pressed={!isMoving}>
          Parado
        </Button>
        <Button onClick={() => onChangeState("moving")} disabled={pending} aria-pressed={isMoving} sx={btnMoving}>
          Movimiento
        </Button>
        <Button onClick={() => setConfirmEnd(true)} disabled={pending} sx={{ ...btnEnd, gridColumn: "1 / -1" }}>
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
          <Button onClick={onEnd} sx={btnEnd}>
            Finalizar
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );

  return (
    <>
      {card}
      <Typography
        sx={{
          fontFamily: display,
          fontSize: 22,
          letterSpacing: "0.02em",
          mb: "18px",
          display: "flex",
          alignItems: "center",
          gap: "10px",
          "&::before": diamond(18, 4, true),
        }}
      >
        Historial de hoy
      </Typography>
      <RideHistory limit={10} reloadKey={endedCount} />
      <StartRideDialog open={startOpen} onClose={() => setStartOpen(false)} onStart={onStart} />
    </>
  );
}
