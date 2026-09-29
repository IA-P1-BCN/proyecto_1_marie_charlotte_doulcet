import { useState } from "react";
import Alert from "@mui/material/Alert";
import CircularProgress from "@mui/material/CircularProgress";
import Typography from "@mui/material/Typography";
import { useTodayRides } from "../../hooks/useTodayRides.js";
import RideDetailDialog from "./RideDetailDialog.jsx";
import RideTable from "./RideTable.jsx";

// Today's rides; click a row for its detail. `limit` caps the list, `reloadKey` forces a refetch.
export default function RideHistory({ limit, reloadKey }) {
  const { rides, loading, error } = useTodayRides({ limit, reloadKey });
  const [selected, setSelected] = useState(null);

  if (loading) {
    return (
      <Typography sx={{ textAlign: "center" }}>
        <CircularProgress />
      </Typography>
    );
  }
  if (error) return <Alert severity="error">No se pudo cargar el historial. Inténtalo de nuevo.</Alert>;
  if (rides.length === 0) return <Typography>No hay carreras registradas hoy.</Typography>;

  return (
    <>
      <RideTable rides={rides} onSelect={setSelected} />
      <RideDetailDialog ride={selected} onClose={() => setSelected(null)} />
    </>
  );
}
