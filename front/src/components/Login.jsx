import { useEffect, useState } from "react";
import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";
import TextField from "@mui/material/TextField";
import Button from "@mui/material/Button";
import Alert from "@mui/material/Alert";
import CircularProgress from "@mui/material/CircularProgress";
import { colors, display, diamond, panelSx, btnMoving } from "../theme.js";
import client from "../api/client.js";
import Header, { Footer } from "./Header.jsx";

// One account per install. Nothing registered yet: first-connection form (company + password twice);
// otherwise: log in with company + password. The password is shared with the CLI/GUI (auth.ini).
export default function Login({ onLogin }) {
  const [registered, setRegistered] = useState(null);
  const [company, setCompany] = useState("");
  const [password, setPassword] = useState("");
  const [confirm, setConfirm] = useState("");
  const [error, setError] = useState("");

  useEffect(() => {
    client
      .get("/auth/status")
      .then(({ data }) => setRegistered(data.registered))
      .catch(() => setError("Sin conexión con el servidor."));
  }, []);

  const submit = async (e) => {
    e.preventDefault();
    setError("");
    if (!registered && password !== confirm) {
      setError("Las contraseñas no coinciden.");
      return;
    }
    try {
      const { data } = await client.post(registered ? "/auth/login" : "/auth/setup", { company, password });
      onLogin(data.token);
    } catch (err) {
      const status = err.response?.status;
      setError(
        status === 401
          ? "Nombre de empresa o contraseña incorrectos."
          : status === 422
            ? "El nombre de la empresa y la contraseña no pueden estar vacíos."
            : "Error de conexión. Inténtalo de nuevo.",
      );
    }
  };

  return (
    <>
      <Header />
      <Box sx={{ maxWidth: 520, mx: "auto", px: { xs: 2, sm: "36px" }, py: { xs: 3, sm: 6 } }}>
        <Box component="form" onSubmit={submit} sx={{ ...panelSx, display: "flex", flexDirection: "column", gap: 2 }}>
          {registered === null && !error ? (
            <CircularProgress sx={{ alignSelf: "center" }} />
          ) : (
            registered !== null && (
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
            )
          )}
          {error && <Alert severity="error">{error}</Alert>}
        </Box>
      </Box>
      <Footer />
    </>
  );
}
