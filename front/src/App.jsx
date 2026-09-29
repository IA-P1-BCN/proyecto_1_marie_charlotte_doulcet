import { useEffect, useState } from "react";
import { Routes, Route, Link, useLocation } from "react-router-dom";
import Box from "@mui/material/Box";
import Tabs from "@mui/material/Tabs";
import Tab from "@mui/material/Tab";
import Button from "@mui/material/Button";
import { colors, display } from "./theme.js";
import ActiveRide from "./components/ActiveRide.jsx";
import RideHistory from "./components/RideHistory.jsx";
import Login from "./components/Login.jsx";
import Header, { Footer } from "./components/Header.jsx";
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
      <Header>
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
      </Header>
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
      <Footer />
    </>
  );
}
