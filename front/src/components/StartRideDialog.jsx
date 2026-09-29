import { useEffect, useState } from "react";
import Dialog from "@mui/material/Dialog";
import DialogTitle from "@mui/material/DialogTitle";
import DialogContent from "@mui/material/DialogContent";
import DialogActions from "@mui/material/DialogActions";
import TextField from "@mui/material/TextField";
import Checkbox from "@mui/material/Checkbox";
import FormControlLabel from "@mui/material/FormControlLabel";
import Button from "@mui/material/Button";
import Alert from "@mui/material/Alert";
import { btnMoving } from "../theme.js";
import client from "../api/client.js";

// Pre-ride step: rates are prefilled with the defaults and only editable here, never mid-ride.
export default function StartRideDialog({ open, onClose, onStart }) {
  const [stopped, setStopped] = useState("");
  const [moving, setMoving] = useState("");
  const [saveDefault, setSaveDefault] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!open) return;
    setError("");
    setSaveDefault(false);
    client
      .get("/rates")
      .then(({ data }) => {
        setStopped(String(data.stopped_rate));
        setMoving(String(data.moving_rate));
      })
      .catch(() => setError("No se pudieron cargar las tarifas."));
  }, [open]);

  const submit = async () => {
    const rates = { stopped_rate: Number(stopped), moving_rate: Number(moving) };
    if (!(rates.stopped_rate > 0) || !(rates.moving_rate > 0)) {
      setError("Las tarifas deben ser números positivos.");
      return;
    }
    try {
      if (saveDefault) await client.put("/rates", rates);
      await onStart(rates);
      onClose();
    } catch {
      setError("No se pudo iniciar la carrera. Inténtalo de nuevo.");
    }
  };

  return (
    <Dialog open={open} onClose={onClose} fullWidth maxWidth="xs">
      <DialogTitle>Tarifas para esta carrera</DialogTitle>
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
        <FormControlLabel
          control={<Checkbox checked={saveDefault} onChange={(e) => setSaveDefault(e.target.checked)} />}
          label="Guardar como tarifas por defecto"
        />
        {error && <Alert severity="error">{error}</Alert>}
      </DialogContent>
      <DialogActions>
        <Button onClick={onClose}>Cancelar</Button>
        <Button onClick={submit} sx={btnMoving}>
          Empezar carrera
        </Button>
      </DialogActions>
    </Dialog>
  );
}
