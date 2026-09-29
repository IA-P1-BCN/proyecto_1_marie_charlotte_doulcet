import time
import logging
import getpass
from taximetro.domain.ride import Ride
from taximetro.infrastructure.storage.file_storage import FileStorage
from taximetro.infrastructure.logging_setup import configure_logging
from taximetro.infrastructure.rates_config import load_rates, save_rates
from taximetro.infrastructure.auth import (hash_password, check_password, is_password_set, save_password_hash, load_password_hash,)

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

def _setup_new_password():
    while True:
        new_password = getpass.getpass("Nueva contraseña: ").strip()
        if not new_password:
            print("La contraseña no puede estar vacía.")
            continue

        confirm_password = getpass.getpass("Confirme la contraseña: ").strip()
        if new_password != confirm_password:
            print("Las contraseñas no coinciden. Intente de nuevo.")
            continue

        save_password_hash(hash_password(new_password))
        return

def require_password():
    if not is_password_set():
        print("No hay contraseña configurada. Configure una para continuar.")
        _setup_new_password()
        logging.info("Password set for the first time")
        return

    stored_hash = load_password_hash()
    if "$" not in stored_hash:
        logging.warning("Stored password hash is malformed, restarting setup")
        print("La contraseña guardada está dañada. Configure una nueva para continuar.")
        _setup_new_password()
        logging.info("Password reset after corrupted hash")
        return
    
    while True:
        try:
            password = getpass.getpass("Contraseña (Q para salir): ").strip()
        except EOFError:
            password = "Q"

        if password.upper() == "Q":
            logging.info("User exited at password prompt")
            print("Saliendo del taxímetro. ¡Hasta luego!")
            raise SystemExit(0)
        
        if check_password(password, stored_hash):
            return 
        print("Contraseña incorrecta. Intente de nuevo.")

def main():
    configure_logging()
    logging.info("Taximetro started")
    require_password()

    try:
        rates = load_rates()
    except ValueError:
        logging.exception("Failed to load rate configuration")
        print("No se pudo cargar la configuración de tarifas. Revise config.ini.")
        return

    storage = FileStorage()
    current_ride = None

    while True:
        print(MENU)
        command = input("Comando: ").strip().upper()

        try:
            if command == "N":
                if current_ride is not None:
                    print("Ya hay una carrera en curso.")
                    continue

                current_ride = Ride(rates)
                print("Carrera iniciada. Estado: parado.")

            elif command in ["M", "P"]:
                if current_ride is None:
                    print("No hay una carrera en curso. Inicie una carrera primero.")
                    continue

                new_state = {"M": "moving", "P": "stopped"}[command]
                estado_es = "en movimiento" if new_state == "moving" else "parado"
                estado_nombre = "movimiento" if new_state == "moving" else "parado"

                if current_ride.state == new_state:
                    print(f"Ya estás en modo {estado_nombre}. Puedes cambiar de estado o finalizar la carrera (F).")
                    continue

                current_ride.toggle_state(new_state)
                logging.info("State changed to %s", new_state)
                print(f"Estado cambiado a: {estado_es}.")

            elif command == "F":
                if current_ride is None:
                    print("No hay una carrera en curso. Inicie una carrera primero.")
                    continue

                total = current_ride.end()
                duration_seconds = current_ride.get_duration_seconds()
                logging.info("Ride ended, duration=%ss, total=%s", duration_seconds, current_ride.format_total())
                print(f"Carrera finalizada. Total a pagar: {current_ride.format_total()} €")

                storage.save_ride(current_ride)
                current_ride = None

            elif command == "T":
                tarifa_input = input("¿Qué tarifa? (P = parado, M = en movimiento): ").strip().upper()
                if tarifa_input not in ("P", "M"):
                    print("Opción no válida. Use P o M.")
                    continue

                rate_key = "stopped_rate" if tarifa_input == "P" else "moving_rate"
                new_value_input = input(f"Nuevo valor para {rate_key} (€/segundo): ").strip()

                try:
                    new_value = float(new_value_input)
                    updated_rates = {**rates, rate_key: new_value}
                    save_rates(updated_rates)
                except ValueError:
                    print("Valor no válido. Debe ser un número positivo. La tarifa actual no ha cambiado.")
                    continue

                rates = updated_rates
                logging.info("Rate changed: %s = %s", rate_key, new_value)
                print(f"Tarifa actualizada: {rate_key} = {new_value} €/segundo")

            elif command == "Q":
                if current_ride is not None:
                    print("Finalice carrera antes de salir...")
                    continue

                print("Saliendo del taxímetro. ¡Hasta luego!")
                return

            elif command == "H":
                rides = storage.load_today()
                if not rides:
                    print("No hay carreras registradas para hoy.")
                else:
                    print("Historial de carreras de hoy:")
                    for ride in rides:
                        print(f"Duración: {ride.get_duration_seconds()} segundos, Monto: {ride.format_total()} €")
            else:
                print("Comando no reconocido. Intente de nuevo.")
        except Exception:
            logging.exception("Unexpected error handling command %s", command)
            print("Ocurrió un error inesperado. Intente de nuevo.")

if __name__ == "__main__":
    main()