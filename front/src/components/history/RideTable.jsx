import Box from "@mui/material/Box";
import Table from "@mui/material/Table";
import TableBody from "@mui/material/TableBody";
import TableCell from "@mui/material/TableCell";
import TableHead from "@mui/material/TableHead";
import TableRow from "@mui/material/TableRow";
import { colors } from "../../theme/tokens.js";
import { cardSx } from "../../theme/styles.js";
import { formatDateTime, formatDuration } from "../../utils/format.js";

const headCell = {
  color: colors.yellow,
  fontSize: 12,
  letterSpacing: "0.08em",
  textTransform: "uppercase",
  fontWeight: 500,
  py: "12px",
  px: "18px",
};

export default function RideTable({ rides, onSelect }) {
  return (
    <Box sx={cardSx}>
      <Table>
        <TableHead>
          <TableRow sx={{ bgcolor: colors.ink }}>
            <TableCell sx={headCell}>Fecha</TableCell>
            <TableCell sx={headCell}>Duración</TableCell>
            <TableCell sx={headCell} align="right">
              Importe
            </TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {rides.map((ride) => (
            <TableRow key={ride.id} hover onClick={() => onSelect(ride)} sx={{ cursor: "pointer" }}>
              <TableCell sx={{ py: 2, px: "18px" }}>{formatDateTime(ride.started_at)}</TableCell>
              <TableCell sx={{ py: 2, px: "18px" }}>{formatDuration(ride.duration_seconds)}</TableCell>
              <TableCell align="right" sx={{ color: colors.pinkText, fontWeight: 600, fontSize: 16, py: 2, px: "18px" }}>
                {ride.amount.toFixed(2)}€
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </Box>
  );
}
