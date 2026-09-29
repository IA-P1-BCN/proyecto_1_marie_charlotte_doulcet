import Button from "@mui/material/Button";
import { colors } from "../../theme/tokens.js";
import { useAuth } from "../../hooks/useAuth.js";

export default function LogoutButton() {
  const { logout } = useAuth();
  return (
    <Button
      onClick={logout}
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
  );
}
