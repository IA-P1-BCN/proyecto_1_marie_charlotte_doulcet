import getpass
import logging
from taximetro.bootstrap import build_auth_service, build_ride_service
from taximetro.domain.errors import AlreadyInStateError, NoActiveRideError, RideAlreadyActiveError
from taximetro.domain.ride_state import RideState
from taximetro.infrastructure.logging_setup import configure_logging

MENU = """
========== TAXIMETRO =========
N - Iniciar carrera
M - Cambiar a en movimiento
P - Cambiar a parado
F - Finalizar carrera
H - Ver historial de hoy
T - Cambiar tarifa
Q - Salir
Ingrese un comando:"""

STATE_LABEL = {RideState.MOVING: "en movimiento", RideState.STOPPED: "parado"}
STATE_NAME = {RideState.MOVING: "movimiento", RideState.STOPPED: "parado"}
STATE_COMMANDS = {"M": RideState.MOVING, "P": RideState.STOPPED}
RATE_KEYS = {"P": "stopped_rate", "M": "moving_rate"}
NO_RIDE = "No hay una carrera en curso. Inicie una carrera primero."


class TaximeterCli:
    """Console presentation layer. Keyboard and screen are injected so tests can script them."""

    def __init__(self, rides, auth, read=input, read_secret=getpass.getpass, write=print):
        self._rides = rides
        self._auth = auth
        self._read = read
        self._read_secret = read_secret
        self._write = write

    def run(self):
        logging.info("Taximetro started")
        if self.require_password():
            self.command_loop()

    # --- password ---
    def require_password(self):
        """Return True when the user may continue, False when they chose to quit."""
        if not self._auth.has_password():
            self._write("No hay contraseña configurada. Configure una para continuar.")
            self._setup_new_password()
            logging.info("Password set for the first time")
            return True
        if not self._auth.has_usable_password():
            logging.warning("Stored password hash is malformed, restarting setup")
            self._write("La contraseña guardada está dañada. Configure una nueva para continuar.")
            self._setup_new_password()
            logging.info("Password reset after corrupted hash")
            return True
        while True:
            try:
                password = self._read_secret("Contraseña (Q para salir): ").strip()
            except EOFError:
                password = "Q"
            if password.upper() == "Q":
                logging.info("User exited at password prompt")
                self._write("Saliendo del taxímetro. ¡Hasta luego!")
                return False
            if self._auth.verify_password(password):
                return True
            self._write("Contraseña incorrecta. Intente de nuevo.")

    def _setup_new_password(self):
        while True:
            new_password = self._read_secret("Nueva contraseña: ").strip()
            if not new_password:
                self._write("La contraseña no puede estar vacía.")
                continue
            if new_password != self._read_secret("Confirme la contraseña: ").strip():
                self._write("Las contraseñas no coinciden. Intente de nuevo.")
                continue
            self._auth.set_password(new_password)
            return

    # --- commands ---
    def command_loop(self):
        while True:
            self._write(MENU)
            command = self._read("Comando: ").strip().upper()
            try:
                if command == "Q" and self._quit():
                    return
                if command != "Q":
                    self._dispatch(command)
            except Exception:
                logging.exception("Unexpected error handling command %s", command)
                self._write("Ocurrió un error inesperado. Intente de nuevo.")

    def _dispatch(self, command):
        if command == "N":
            self._start_ride()
        elif command in STATE_COMMANDS:
            self._change_state(STATE_COMMANDS[command])
        elif command == "F":
            self._end_ride()
        elif command == "T":
            self._change_rate()
        elif command == "H":
            self._show_history()
        else:
            self._write("Comando no reconocido. Intente de nuevo.")

    def _start_ride(self):
        try:
            self._rides.start_ride()
            self._write("Carrera iniciada. Estado: parado.")
        except RideAlreadyActiveError:
            self._write("Ya hay una carrera en curso.")

    def _change_state(self, new_state):
        try:
            self._rides.change_state(new_state)
            self._write(f"Estado cambiado a: {STATE_LABEL[new_state]}.")
        except NoActiveRideError:
            self._write(NO_RIDE)
        except AlreadyInStateError:
            self._write(
                f"Ya estás en modo {STATE_NAME[new_state]}. Puedes cambiar de estado o finalizar la carrera (F)."
            )

    def _end_ride(self):
        try:
            record = self._rides.end_ride()
        except NoActiveRideError:
            self._write(NO_RIDE)
            return
        logging.info("Ride ended, duration=%ss, total=%.2f", round(record.duration_seconds), record.amount)
        self._write(f"Carrera finalizada. Total a pagar: {record.amount:.2f} €")

    def _change_rate(self):
        choice = self._read("¿Qué tarifa? (P = parado, M = en movimiento): ").strip().upper()
        if choice not in RATE_KEYS:
            self._write("Opción no válida. Use P o M.")
            return
        rate_key = RATE_KEYS[choice]
        raw_value = self._read(f"Nuevo valor para {rate_key} (€/segundo): ").strip()
        try:
            new_value = float(raw_value)
            self._rides.change_rate(rate_key, new_value)
        except ValueError:
            self._write("Valor no válido. Debe ser un número positivo. La tarifa actual no ha cambiado.")
            return
        logging.info("Rate changed: %s = %s", rate_key, new_value)
        self._write(f"Tarifa actualizada: {rate_key} = {new_value} €/segundo")

    def _show_history(self):
        records = self._rides.get_today_history()
        if not records:
            self._write("No hay carreras registradas para hoy.")
            return
        self._write("Historial de carreras de hoy:")
        for record in records:
            self._write(f"Duración: {round(record.duration_seconds)} segundos, Monto: {record.amount:.2f} €")

    def _quit(self):
        if self._rides.has_active_ride:
            self._write("Finalice carrera antes de salir...")
            return False
        self._write("Saliendo del taxímetro. ¡Hasta luego!")
        return True


def main():
    configure_logging()
    try:
        rides = build_ride_service()
    except ValueError:
        logging.exception("Failed to load rate configuration")
        print("No se pudo cargar la configuración de tarifas. Revise config.ini.")
        return
    TaximeterCli(rides, build_auth_service()).run()


if __name__ == "__main__":
    main()
