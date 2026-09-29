import { useCallback, useEffect, useState } from "react";
import { changeRideState, endRide, getActiveRide, startRide } from "../services/rideService.js";

const REFRESH_MS = 1000;
const GENERIC_ERROR = "Error de conexión. Inténtalo de nuevo.";
const NO_RIDE = "No hay una carrera en curso.";

// Polls the single ride in progress and exposes the actions that change it.
export function useActiveRide() {
  const [ride, setRide] = useState(null);
  const [loading, setLoading] = useState(true);
  const [pending, setPending] = useState(false);
  const [message, setMessage] = useState("");
  const [endedCount, setEndedCount] = useState(0);

  const refresh = useCallback(async () => {
    try {
      setRide(await getActiveRide());
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
    refresh();
    // ponytail: a stale poll response can land after a start/state/end action and
    // overwrite it for up to REFRESH_MS. Add a request counter if that flicker matters.
    const id = setInterval(refresh, REFRESH_MS);
    return () => clearInterval(id);
  }, [refresh]);

  // Runs one action with the shared pending flag; `onError` maps an HTTP status to a message.
  const run = async (action, onSuccess, errorFor) => {
    setPending(true);
    try {
      onSuccess(await action());
    } catch (err) {
      setMessage(errorFor(err.response?.status) ?? GENERIC_ERROR);
    } finally {
      setPending(false);
    }
  };

  const start = (rates) =>
    run(
      () => startRide(rates),
      (data) => {
        setRide(data);
        setMessage("");
      },
      (status) => (status === 409 ? "Ya hay una carrera en curso." : null),
    );

  const changeState = (state) =>
    run(
      () => changeRideState(state),
      (data) => {
        setRide(data);
        setMessage("");
      },
      (status) => (status === 409 ? "Ya estás en ese estado." : status === 404 ? NO_RIDE : null),
    );

  const end = () =>
    run(
      endRide,
      () => {
        setRide(null);
        setEndedCount((n) => n + 1);
        setMessage("Carrera finalizada.");
      },
      (status) => (status === 404 ? NO_RIDE : null),
    );

  return { ride, loading, pending, message, endedCount, start, changeState, end };
}
