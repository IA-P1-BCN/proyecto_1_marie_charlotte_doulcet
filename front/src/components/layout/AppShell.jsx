import { Outlet } from "react-router-dom";
import Box from "@mui/material/Box";
import Footer from "./Footer.jsx";
import Header from "./Header.jsx";
import LogoutButton from "./LogoutButton.jsx";
import NavTabs from "./NavTabs.jsx";

// Frame of every authenticated screen: header, tabs, page content (Outlet), footer.
export default function AppShell() {
  return (
    <>
      <Header>
        <LogoutButton />
      </Header>
      <NavTabs />
      <Box component="main" sx={{ maxWidth: 760, mx: "auto", px: { xs: 2, sm: "36px" }, py: { xs: 3, sm: 6 } }}>
        <Outlet />
      </Box>
      <Footer />
    </>
  );
}
