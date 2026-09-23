import time 
import logging
from datetime import date
from taximetro.pricing import calculate_segment, format_amount
from taximetro.history import append_ride, load_today_rides
from taximetro.logging_setup import configure_logging
from taximetro.rates_config import load_rates, save_rates

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

def toggle_state(command, state, start_timestamp, total, rates, now=None):
    new_state = {"M" : "moving", "P": "stopped"}[command]
    if new_state == state:
        return state, start_timestamp, total

    now = now if now is not None else time.time()
    elapsed = now - start_timestamp
    total += calculate_segment(state, elapsed, rates)
    return new_state, now, total

def main():
    configure_logging()
    logging.info("Taximetro started")

    try:
        rates = load_rates()
    except ValueError:
        logging.exception("Failed to load rate configuration")
        print("No se pudo cargar la configuración de tarifas. Revise config.ini.")
        return
    
    ride_active = False 
    state = None
    start_timestamp = None
    ride_start_timestamp = None
    total = 0.0

    while True:
        print(MENU)
        command = input("Comando: ").strip().upper()

        try:
            if command == "N":
                if ride_active:
                    print("Ya hay una carrera en curso.") 
                    continue 

                ride_active = True
                state = "stopped"
                start_timestamp = time.time()
                ride_start_timestamp = start_timestamp
                total = 0.0
                print("Carrera iniciada. Estado: parado.")

            elif command in ["M", "P"]:
                if not ride_active:
                    print("No hay una carrera en curso. Inicie una carrera primero.")
                    continue

                state, start_timestamp, total = toggle_state(
                    command, state, start_timestamp, total, rates
                )
                logging.info("State changed to %s", state)
                estado_es = "en movimiento" if state == "moving" else "parado"
                print(f"Estado cambiado a: {estado_es}.")

            elif command == "F":
                if not ride_active:
                    print("No hay una carrera en curso. Inicie una carrera primero.")
                    continue

                now = time.time()
                total += calculate_segment(state, now - start_timestamp, rates)
                duration_seconds = round(now - ride_start_timestamp)
                ride_active = False
                logging.info("Ride ended, duration=%ss, total=%s", duration_seconds, format_amount(total))
                print(f"Carrera finalizada. Total a pagar: {format_amount(total)} €")
                append_ride({
                    "date": date.today().isoformat(),
                    "duration_seconds": str(duration_seconds),
                    "amount": format_amount(total)
                })
                state = None
                start_timestamp = None
                ride_start_timestamp = None
                total = 0.0

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
                except ValueError as e:
                    print("Valor no válido. Debe ser un número positivo. La tarifa actual no ha cambiado.")
                    continue

                rates = updated_rates
                logging.info("Rate changed: %s = %s", rate_key, new_value)
                print(f"Tarifa actualizada: {rate_key} = {new_value} €/segundo")

            elif command == "Q":
                if ride_active:
                    print("Finalice carrera antes de salir...")
                    continue

                print("Saliendo del taxímetro. ¡Hasta luego!")
                return

            elif command == "H":
                rides = load_today_rides()
                if not rides:
                    print("No hay carreras registradas para hoy.")
                else:
                    print("Historial de carreras de hoy:")
                    for ride in rides:
                        print(f"Fecha: {ride['date']}, Duración: {ride['duration_seconds']} segundos, Monto: {ride['amount']} €")
            else:
                print("Comando no reconocido. Intente de nuevo.")
        except Exception:
            logging.exception("Unexpected error handling command %s", command)
            print("Ocurrió un error inesperado. Intente de nuevo.")

if __name__ == "__main__":
    main()
