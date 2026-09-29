import { Link, useLocation } from "react-router-dom";
import Tab from "@mui/material/Tab";
import Tabs from "@mui/material/Tabs";
import { colors, display } from "../../theme/tokens.js";

export default function NavTabs() {
  const { pathname } = useLocation();
  return (
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
  );
}
