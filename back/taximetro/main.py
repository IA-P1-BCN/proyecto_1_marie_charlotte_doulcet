import time 
from datetime import date
from taximetro.pricing import calculate_segment, format_amount
from taximetro.history import append_ride, load_today_rides

RATES = {"stopped_rate": 0.02, "moving_rate": 0.05}

MENU = """
========== TAXIMETRO =========
N - Iniciar carrera
M - Cambiar a en movimiento
P - Cambiar a parado
F - Finalizar carrera
H - Ver historial de hoy
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
    ride_active = False 
    state = None
    start_timestamp = None
    ride_start_timestamp = None
    total = 0.0

    while True:
        print(MENU)
        command = input("Comando: ").strip().upper()

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
                command, state, start_timestamp, total, RATES
            )
            estado_es = "en movimiento" if state == "moving" else "parado"
            print(f"Estado cambiado a: {estado_es}.")

        elif command == "F":
            if not ride_active:
                print("No hay una carrera en curso. Inicie una carrera primero.")
                continue

            now = time.time()
            total += calculate_segment(state, now - start_timestamp, RATES)
            duration_seconds = round(now - ride_start_timestamp)
            ride_active = False
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

if __name__ == "__main__":
    main()
