import { useEffect, useState } from "react";
import { getAuthStatus, login, register } from "../services/authService.js";
import { useAuth } from "./useAuth.js";

const errorMessage = (status) =>
  status === 401
    ? "Nombre de empresa o contraseña incorrectos."
    : status === 422
      ? "El nombre de la empresa y la contraseña no pueden estar vacíos."
      : "Error de conexión. Inténtalo de nuevo.";

export function useAuthFlow() {
  const { login: startSession } = useAuth();
  const [registered, setRegistered] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    getAuthStatus()
      .then(setRegistered)
      .catch(() => setError("Sin conexión con el servidor."));
  }, []);

  const submit = async ({ company, password, confirm }) => {
    setError("");
    if (!registered && password !== confirm) {
      setError("Las contraseñas no coinciden.");
      return;
    }
    try {
      const token = await (registered ? login : register)({ company, password });
      startSession(token);
    } catch (err) {
      setError(errorMessage(err.response?.status));
    }
  };

  return { registered, error, submit };
}
