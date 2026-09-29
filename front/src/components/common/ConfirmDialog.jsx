import Button from "@mui/material/Button";
import Dialog from "@mui/material/Dialog";
import DialogActions from "@mui/material/DialogActions";
import DialogTitle from "@mui/material/DialogTitle";
import { btnEnd } from "../../theme/styles.js";

// In-app confirmation (never window.confirm).
export default function ConfirmDialog({ open, title, confirmLabel, onConfirm, onCancel }) {
  return (
    <Dialog open={open} onClose={onCancel}>
      <DialogTitle>{title}</DialogTitle>
      <DialogActions>
        <Button onClick={onCancel}>Cancelar</Button>
        <Button onClick={onConfirm} sx={btnEnd}>
          {confirmLabel}
        </Button>
      </DialogActions>
    </Dialog>
  );
}
