import { Route, Routes } from "react-router-dom";
import AppShell from "../components/layout/AppShell.jsx";
import { useAuth } from "../hooks/useAuth.js";
import HistoryPage from "../pages/HistoryPage.jsx";
import RidePage from "../pages/RidePage.jsx";
import WelcomePage from "../pages/WelcomePage.jsx";

export default function AppRoutes() {
  const { isAuthenticated } = useAuth();
  if (!isAuthenticated) return <WelcomePage />;

  return (
    <Routes>
      <Route element={<AppShell />}>
        <Route path="/" element={<RidePage />} />
        <Route path="/historial" element={<HistoryPage />} />
      </Route>
    </Routes>
  );
}
