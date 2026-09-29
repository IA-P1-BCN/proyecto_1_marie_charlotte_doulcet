import { useEffect, useState } from "react";
import { getTodayRides } from "../services/rideService.js";

export function useTodayRides({ limit, reloadKey = 0 } = {}) {
  const [rides, setRides] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);

  useEffect(() => {
    getTodayRides()
      .then((data) => {
        const newestFirst = [...data].sort((a, b) => b.started_at.localeCompare(a.started_at));
        setRides(limit ? newestFirst.slice(0, limit) : newestFirst);
        setError(false);
      })
      .catch(() => setError(true))
      .finally(() => setLoading(false));
  }, [limit, reloadKey]);

  return { rides, loading, error };
}
