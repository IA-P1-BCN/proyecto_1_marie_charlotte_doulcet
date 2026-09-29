import { useState } from "react";
import Box from "@mui/material/Box";
import Button from "@mui/material/Button";
import ConfirmDialog from "../common/ConfirmDialog.jsx";
import { btnEnd, btnMoving } from "../../theme/styles.js";
import { RIDE_STATE } from "../../utils/rideState.js";

export default function RideControls({ state, pending, onChangeState, onEnd }) {
  const [confirmEnd, setConfirmEnd] = useState(false);
  const isMoving = state === RIDE_STATE.MOVING;

  return (
    <Box sx={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "12px" }}>
      <Button onClick={() => onChangeState(RIDE_STATE.STOPPED)} disabled={pending} aria-pressed={!isMoving}>
        Parado
      </Button>
      <Button
        onClick={() => onChangeState(RIDE_STATE.MOVING)}
        disabled={pending}
        aria-pressed={isMoving}
        sx={btnMoving}
      >
        Movimiento
      </Button>
      <Button onClick={() => setConfirmEnd(true)} disabled={pending} sx={{ ...btnEnd, gridColumn: "1 / -1" }}>
        Fin de carrera
      </Button>
      <ConfirmDialog
        open={confirmEnd}
        title="¿Finalizar la carrera actual?"
        confirmLabel="Finalizar"
        onCancel={() => setConfirmEnd(false)}
        onConfirm={() => {
          setConfirmEnd(false);
          onEnd();
        }}
      />
    </Box>
  );
}
