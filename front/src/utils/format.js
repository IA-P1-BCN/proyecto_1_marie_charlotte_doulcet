export function formatDuration(seconds) {
  const total = Math.round(seconds);
  const h = String(Math.floor(total / 3600)).padStart(2, "0");
  const m = String(Math.floor((total % 3600) / 60)).padStart(2, "0");
  const s = String(total % 60).padStart(2, "0");
  return `${h}:${m}:${s}`;
}

export const formatDateTime = (iso) => iso.replace("T", " ").slice(0, 16);
