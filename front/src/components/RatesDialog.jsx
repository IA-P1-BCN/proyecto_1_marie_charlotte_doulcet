import { useEffect, useState } from "react";
import Dialog from "@mui/material/Dialog";
import DialogTitle from "@mui/material/DialogTitle";
import DialogContent from "@mui/material/DialogContent";
import DialogActions from "@mui/material/DialogActions";
import TextField from "@mui/material/TextField";
import Button from "@mui/material/Button";
import Alert from "@mui/material/Alert";
import { colors } from "../theme.js";
import client from "../api/client.js";

export default function RatesDialog({ open, onClose, onSaved }) {
  const [stopped, setStopped] = useState("");
  const [moving, setMoving] = useState("");
  const [error, setError] = useState("");

  useEffect(() => {
    if (!open) return;
    setError("");
    client.get("/rates").then(({ data }) => {
      setStopped(String(data.stopped_rate));
      setMoving(String(data.moving_rate));
    });
  }, [open]);

  const save = async () => {
    const stopped_rate = Number(stopped);
    const moving_rate = Number(moving);
    if (!(stopped_rate > 0) || !(moving_rate > 0)) {
      setError("Las tarifas deben ser números positivos.");
      return;
    }
    try {
      const { data } = await client.put("/rates", { stopped_rate, moving_rate });
      onSaved(data);
      onClose();
    } catch {
      setError("No se pudo guardar la tarifa. Inténtalo de nuevo.");
    }
  };

  return (
    <Dialog open={open} onClose={onClose} fullWidth maxWidth="xs">
      <DialogTitle>Cambiar tarifa</DialogTitle>
      <DialogContent sx={{ display: "flex", flexDirection: "column", gap: 2, pt: "8px !important" }}>
        <TextField
          label="Parado (€/s)"
          type="number"
          value={stopped}
          onChange={(e) => setStopped(e.target.value)}
          slotProps={{ htmlInput: { step: "0.01", min: "0" } }}
        />
        <TextField
          label="Movimiento (€/s)"
          type="number"
          value={moving}
          onChange={(e) => setMoving(e.target.value)}
          slotProps={{ htmlInput: { step: "0.01", min: "0" } }}
        />
        {error && <Alert severity="error">{error}</Alert>}
        <Alert severity="info">Se aplica a partir de la próxima carrera.</Alert>
      </DialogContent>
      <DialogActions>
        <Button onClick={onClose}>Cancelar</Button>
        <Button variant="contained" onClick={save} sx={{ bgcolor: colors.pinkText }}>
          Guardar
        </Button>
      </DialogActions>
    </Dialog>
  );
}
