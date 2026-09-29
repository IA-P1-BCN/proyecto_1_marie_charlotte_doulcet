import { useEffect, useState } from "react";
import { getRates } from "../services/ratesService.js";

// Loads the default rates each time `active` turns true (used to prefill the pre-ride dialog).
export function useDefaultRates(active) {
  const [rates, setRates] = useState(null);
  const [error, setError] = useState(false);

  useEffect(() => {
    if (!active) return;
    setError(false);
    getRates()
      .then(setRates)
      .catch(() => setError(true));
  }, [active]);

  return { rates, error };
}
