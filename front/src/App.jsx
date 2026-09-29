import { Routes, Route, Link, useLocation } from "react-router-dom";
import AppBar from "@mui/material/AppBar";
import Toolbar from "@mui/material/Toolbar";
import Tabs from "@mui/material/Tabs";
import Tab from "@mui/material/Tab";
import Typography from "@mui/material/Typography";
import Container from "@mui/material/Container";
import { colors } from "./theme.js";
import ActiveRide from "./components/ActiveRide.jsx";
import RideHistory from "./components/RideHistory.jsx";

export default function App() {
  const { pathname } = useLocation();

  return (
    <>
      <AppBar position="static" sx={{ bgcolor: colors.ink }}>
        <Toolbar>
          <Typography sx={{ color: colors.yellow, fontFamily: "'Bebas Neue', sans-serif", fontSize: 28 }}>
            TaxiTech
          </Typography>
        </Toolbar>
      </AppBar>
      <Tabs
        value={pathname}
        sx={{
          bgcolor: colors.yellow,
          "& .MuiTab-root": { color: colors.tabInactive, opacity: 1 },
          "& .Mui-selected": { bgcolor: colors.ink, color: `${colors.yellow} !important` },
        }}
      >
        <Tab label="Carrera activa" value="/" component={Link} to="/" />
        <Tab label="Historial" value="/historial" component={Link} to="/historial" />
      </Tabs>
      <Container maxWidth="sm" sx={{ py: 4 }}>
        <Routes>
          <Route path="/" element={<ActiveRide />} />
          <Route path="/historial" element={<RideHistory />} />
        </Routes>
      </Container>
    </>
  );
}
