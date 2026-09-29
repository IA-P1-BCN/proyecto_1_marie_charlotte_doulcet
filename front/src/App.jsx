import { useEffect, useState } from "react";
import { Routes, Route, Link, useLocation } from "react-router-dom";
import Box from "@mui/material/Box";
import Tabs from "@mui/material/Tabs";
import Tab from "@mui/material/Tab";
import Typography from "@mui/material/Typography";
import Button from "@mui/material/Button";
import { colors, display, diamond } from "./theme.js";
import ActiveRide from "./components/ActiveRide.jsx";
import RideHistory from "./components/RideHistory.jsx";
import Login from "./components/Login.jsx";
import { getToken, setToken, clearToken, AUTH_EXPIRED } from "./auth.js";

export default function App() {
  const { pathname } = useLocation();
  const [token, setTokenState] = useState(getToken);

  useEffect(() => {
    const expire = () => setTokenState(null);
    window.addEventListener(AUTH_EXPIRED, expire);
    return () => window.removeEventListener(AUTH_EXPIRED, expire);
  }, []);

  if (!token) {
    return (
      <Login
        onLogin={(t) => {
          setToken(t);
          setTokenState(t);
        }}
      />
    );
  }

  return (
    <>
      <Box
        component="header"
        sx={{
          bgcolor: colors.ink,
          px: { xs: 2, sm: "36px" },
          py: "22px",
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
          gap: 2,
        }}
      >
        <Typography
          sx={{
            fontFamily: display,
            fontSize: 32,
            letterSpacing: "0.03em",
            color: colors.yellow,
            display: "flex",
            alignItems: "center",
            gap: "10px",
            "&::before": diamond(14, 3),
          }}
        >
          TaxiTech
        </Typography>
        <Box sx={{ display: "flex", alignItems: "center", gap: 2 }}>
          <Typography sx={{ color: colors.bg, fontSize: 11, letterSpacing: "0.15em", textTransform: "uppercase", opacity: 0.6, display: { xs: "none", sm: "block" } }}>
            Digital Taximeter
          </Typography>
          <Button
            onClick={() => {
              clearToken();
              setTokenState(null);
            }}
            sx={{
              color: colors.yellow,
              bgcolor: "transparent",
              border: `2px solid ${colors.yellow}`,
              borderRadius: "8px",
              fontSize: 14,
              lineHeight: 1.2,
              p: "4px 12px",
              "&:hover": { bgcolor: "transparent", filter: "brightness(1.1)" },
            }}
          >
            Cerrar sesión
          </Button>
        </Box>
      </Box>
      <Tabs
        value={pathname}
        slotProps={{ indicator: { sx: { display: "none" } } }}
        sx={{
          bgcolor: colors.yellow,
          px: { xs: 0, sm: "36px" },
          minHeight: 0,
          borderBottom: `4px solid ${colors.ink}`,
          "& .MuiTab-root": {
            fontFamily: display,
            fontSize: 18,
            letterSpacing: "0.03em",
            textTransform: "none",
            minHeight: 0,
            p: "10px 20px",
            color: colors.tabInactive,
            opacity: 1,
          },
          "& .Mui-selected": { bgcolor: colors.ink, color: `${colors.yellow} !important` },
        }}
      >
        <Tab label="Carrera activa" value="/" component={Link} to="/" />
        <Tab label="Historial" value="/historial" component={Link} to="/historial" />
      </Tabs>
      <Box component="main" sx={{ maxWidth: 760, mx: "auto", px: { xs: 2, sm: "36px" }, py: { xs: 3, sm: 6 } }}>
        <Routes>
          <Route path="/" element={<ActiveRide />} />
          <Route path="/historial" element={<RideHistory />} />
        </Routes>
      </Box>
      <Typography component="footer" sx={{ textAlign: "center", p: 4, fontSize: 11, color: colors.muted, letterSpacing: "0.1em", textTransform: "uppercase" }}>
        TaxiTech Solutions · Digital Taximeter
      </Typography>
    </>
  );
}
