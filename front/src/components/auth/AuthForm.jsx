import { useState } from "react";
import Alert from "@mui/material/Alert";
import Box from "@mui/material/Box";
import Button from "@mui/material/Button";
import CircularProgress from "@mui/material/CircularProgress";
import TextField from "@mui/material/TextField";
import Typography from "@mui/material/Typography";
import { colors, display } from "../../theme/tokens.js";
import { btnMoving, diamond, panelSx } from "../../theme/styles.js";

// `registered` null = still asking the server. false = first connection (password typed twice).
export default function AuthForm({ registered, error, onSubmit }) {
  const [company, setCompany] = useState("");
  const [password, setPassword] = useState("");
  const [confirm, setConfirm] = useState("");

  const submit = (e) => {
    e.preventDefault();
    onSubmit({ company, password, confirm });
  };

  return (
    <Box component="form" onSubmit={submit} sx={{ ...panelSx, display: "flex", flexDirection: "column", gap: 2 }}>
      {registered === null && !error && <CircularProgress sx={{ alignSelf: "center" }} />}
      {registered !== null && (
        <>
          <Box>
            <Typography
              component="h1"
              sx={{
                fontFamily: display,
                fontSize: 34,
                lineHeight: 1.1,
                display: "flex",
                alignItems: "center",
                gap: "12px",
                "&::before": { ...diamond(18, 4, true), flexShrink: 0 },
              }}
            >
              {registered ? "Bienvenido de nuevo" : "Bienvenido a TaxiTech"}
            </Typography>
            <Typography sx={{ color: colors.muted, fontSize: 13, mt: 1 }}>
              {registered ? "Inicia sesión con tu empresa." : "Primera conexión"}
            </Typography>
          </Box>
          <TextField
            label="Nombre de la empresa"
            autoComplete="username"
            autoFocus
            value={company}
            onChange={(e) => setCompany(e.target.value)}
          />
          <TextField
            label="Contraseña"
            type="password"
            autoComplete={registered ? "current-password" : "new-password"}
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
          {!registered && (
            <TextField
              label="Repetir contraseña"
              type="password"
              autoComplete="new-password"
              value={confirm}
              onChange={(e) => setConfirm(e.target.value)}
            />
          )}
          <Button type="submit" sx={btnMoving}>
            {registered ? "Entrar" : "Crear cuenta y entrar"}
          </Button>
        </>
      )}
      {error && <Alert severity="error">{error}</Alert>}
    </Box>
  );
}
