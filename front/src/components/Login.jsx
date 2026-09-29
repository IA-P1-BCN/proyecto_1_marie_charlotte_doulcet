import { useEffect, useState } from "react";
import Paper from "@mui/material/Paper";
import Typography from "@mui/material/Typography";
import TextField from "@mui/material/TextField";
import Button from "@mui/material/Button";
import Alert from "@mui/material/Alert";
import CircularProgress from "@mui/material/CircularProgress";
import Container from "@mui/material/Container";
import { colors, btnMoving } from "../theme.js";
import client from "../api/client.js";

// Same password as the CLI/GUI (auth.ini). First use: create it; afterwards: log in.
export default function Login({ onLogin }) {
  const [passwordSet, setPasswordSet] = useState(null);
  const [password, setPassword] = useState("");
  const [confirm, setConfirm] = useState("");
  const [error, setError] = useState("");

  useEffect(() => {
    client
      .get("/auth/status")
      .then(({ data }) => setPasswordSet(data.password_set))
      .catch(() => setError("Sin conexión con el servidor."));
  }, []);

  const submit = async (e) => {
    e.preventDefault();
    setError("");
    if (!passwordSet && password !== confirm) {
      setError("Las contraseñas no coinciden.");
      return;
    }
    try {
      const { data } = await client.post(passwordSet ? "/auth/login" : "/auth/setup", { password });
      onLogin(data.token);
    } catch (err) {
      const status = err.response?.status;
      setError(
        status === 401 ? "Contraseña incorrecta." : status === 422 ? "La contraseña no puede estar vacía." : "Error de conexión. Inténtalo de nuevo.",
      );
    }
  };

  return (
    <Container maxWidth="xs" sx={{ py: 8 }}>
      <Paper component="form" onSubmit={submit} sx={{ p: 4, display: "flex", flexDirection: "column", gap: 2 }}>
        <Typography sx={{ fontFamily: "'Bebas Neue', sans-serif", fontSize: 40 }}>
          {passwordSet === false ? "Crear contraseña" : "TaxiTech"}
        </Typography>
        {passwordSet === null && !error ? (
          <CircularProgress sx={{ alignSelf: "center" }} />
        ) : (
          passwordSet !== null && (
            <>
              <TextField
                label="Contraseña"
                type="password"
                autoFocus
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
              {!passwordSet && (
                <TextField
                  label="Confirmar contraseña"
                  type="password"
                  value={confirm}
                  onChange={(e) => setConfirm(e.target.value)}
                />
              )}
              <Button type="submit" sx={btnMoving}>
                {passwordSet ? "Entrar" : "Crear contraseña"}
              </Button>
            </>
          )
        )}
        {error && <Alert severity="error">{error}</Alert>}
      </Paper>
    </Container>
  );
}
