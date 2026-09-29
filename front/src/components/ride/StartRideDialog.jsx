import { useEffect, useState } from "react";
import Alert from "@mui/material/Alert";
import Button from "@mui/material/Button";
import Checkbox from "@mui/material/Checkbox";
import Dialog from "@mui/material/Dialog";
import DialogActions from "@mui/material/DialogActions";
import DialogContent from "@mui/material/DialogContent";
import DialogTitle from "@mui/material/DialogTitle";
import FormControlLabel from "@mui/material/FormControlLabel";
import TextField from "@mui/material/TextField";
import { useDefaultRates } from "../../hooks/useDefaultRates.js";
import { saveRates } from "../../services/ratesService.js";
import { btnMoving } from "../../theme/styles.js";

const rateInput = { htmlInput: { step: "0.01", min: "0" } };

// Pre-ride step: rates are prefilled with the defaults and only editable here, never mid-ride.
export default function StartRideDialog({ open, onClose, onStart }) {
  const { rates, error: loadError } = useDefaultRates(open);
  const [stopped, setStopped] = useState("");
  const [moving, setMoving] = useState("");
  const [saveDefault, setSaveDefault] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!open) return;
    setError("");
    setSaveDefault(false);
  }, [open]);

  useEffect(() => {
    if (!rates) return;
    setStopped(String(rates.stopped_rate));
    setMoving(String(rates.moving_rate));
  }, [rates]);

  const submit = async () => {
    const chosen = { stopped_rate: Number(stopped), moving_rate: Number(moving) };
    if (!(chosen.stopped_rate > 0) || !(chosen.moving_rate > 0)) {
      setError("Las tarifas deben ser números positivos.");
      return;
    }
    try {
      if (saveDefault) await saveRates(chosen);
      await onStart(chosen);
      onClose();
    } catch {
      setError("No se pudo iniciar la carrera. Inténtalo de nuevo.");
    }
  };

  const shownError = error || (loadError ? "No se pudieron cargar las tarifas." : "");

  return (
    <Dialog open={open} onClose={onClose} fullWidth maxWidth="xs">
      <DialogTitle>Tarifas para esta carrera</DialogTitle>
      <DialogContent sx={{ display: "flex", flexDirection: "column", gap: 2, pt: "8px !important" }}>
        <TextField
          label="Parado (€/s)"
          type="number"
          value={stopped}
          onChange={(e) => setStopped(e.target.value)}
          slotProps={rateInput}
        />
        <TextField
          label="Movimiento (€/s)"
          type="number"
          value={moving}
          onChange={(e) => setMoving(e.target.value)}
          slotProps={rateInput}
        />
        <FormControlLabel
          control={<Checkbox checked={saveDefault} onChange={(e) => setSaveDefault(e.target.checked)} />}
          label="Guardar como tarifas por defecto"
        />
        {shownError && <Alert severity="error">{shownError}</Alert>}
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
