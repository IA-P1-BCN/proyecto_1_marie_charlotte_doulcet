import Box from "@mui/material/Box";
import AuthForm from "../components/auth/AuthForm.jsx";
import Footer from "../components/layout/Footer.jsx";
import Header from "../components/layout/Header.jsx";
import { useAuthFlow } from "../hooks/useAuthFlow.js";

// One account per install: first connection registers it, afterwards it is a plain login.
export default function WelcomePage() {
  const { registered, error, submit } = useAuthFlow();
  return (
    <>
      <Header />
      <Box sx={{ maxWidth: 520, mx: "auto", px: { xs: 2, sm: "36px" }, py: { xs: 3, sm: 6 } }}>
        <AuthForm registered={registered} error={error} onSubmit={submit} />
      </Box>
      <Footer />
    </>
  );
}
