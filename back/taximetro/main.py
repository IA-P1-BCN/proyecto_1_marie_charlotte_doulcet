import time 

MENU = """
========== TAXIMETRO =========
N - Iniciar carrera"""

def main():
    ride_active = False 
    state = None
    start_timestamp = None

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
            print("Carrera iniciada. Estado: parado.")
        else:
            print("Comando no reconocido. Por favor, intente de nuevo.")

if __name__ == "__main__":
    main()
