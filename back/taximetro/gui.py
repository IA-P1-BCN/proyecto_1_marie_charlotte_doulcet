import tkinter as tk
from taximetro.infrastructure.storage.file_storage import FileStorage
from taximetro.infrastructure.rates_config import load_rates
from taximetro.ride_session import RideSession, NoActiveRideError, RideAlreadyActiveError, AlreadyInStateError

COLOR_STOPPED = "#E53935"
COLOR_MOVING = "#43A047"
COLOR_PRIMARY = "#1E88E5"
COLOR_BG = "#F7F7F5"
COLOR_NO_RIDE = "#6B6B6B"

REFRESH_MS = 500


class TaximetroGUI:
    def __init__(self, root, session):
        self.root = root
        self.session = session
        self.root.title("Taxímetro")
        self.root.configure(bg=COLOR_BG)

        self.banner = tk.Label(
            root, text="SIN CARRERA ACTIVA", bg=COLOR_NO_RIDE, fg="white",
            font=("TkDefaultFont", 20, "bold"), pady=12,
        )
        self.banner.pack(fill="x")

        self.amount_label = tk.Label(
            root, text="0.00 €", bg=COLOR_BG, fg="#212121",
            font=("TkDefaultFont", 36, "bold"),
        )
        self.amount_label.pack(pady=24)

        button_frame = tk.Frame(root, bg=COLOR_BG)
        button_frame.pack(pady=8)

        self.start_button = tk.Button(
            button_frame, text="INICIAR CARRERA", bg=COLOR_PRIMARY, fg="white",
            font=("TkDefaultFont", 14, "bold"), width=16, height=2, command=self.on_start,
        )
        self.start_button.grid(row=0, column=0, columnspan=2, padx=8, pady=8)

        self.stopped_button = tk.Button(
            button_frame, text="PARADO", bg=COLOR_STOPPED, fg="white",
            font=("TkDefaultFont", 14, "bold"), width=12, height=2, command=self.on_stopped,
        )
        self.stopped_button.grid(row=1, column=0, padx=8, pady=8)

        self.moving_button = tk.Button(
            button_frame, text="MOVIMIENTO", bg=COLOR_MOVING, fg="white",
            font=("TkDefaultFont", 14, "bold"), width=12, height=2, command=self.on_moving,
        )
        self.moving_button.grid(row=1, column=1, padx=8, pady=8)

        self.end_button = tk.Button(
            root, text="FIN DE CARRERA", bg=COLOR_STOPPED, fg="white",
            font=("TkDefaultFont", 14, "bold"), width=20, height=2, command=self.on_end,
        )
        self.end_button.pack(pady=16)

        self.status_label = tk.Label(
            root, text="", bg=COLOR_BG, fg="#6B6B6B", font=("TkDefaultFont", 10),
        )
        self.status_label.pack(pady=4)

        self.refresh()

    def on_start(self):
        try:
            self.session.start_ride()
            self.status_label.config(text="Carrera iniciada.")
        except RideAlreadyActiveError:
            self.status_label.config(text="Ya hay una carrera en curso.")

    def on_stopped(self):
        self._change_state("stopped")

    def on_moving(self):
        self._change_state("moving")

    def _change_state(self, new_state):
        try:
            self.session.change_state(new_state)
            self.status_label.config(text="")
        except NoActiveRideError:
            self.status_label.config(text="No hay una carrera en curso. Inicie una carrera primero.")
        except AlreadyInStateError:
            estado = "movimiento" if new_state == "moving" else "parado"
            self.status_label.config(text=f"Ya estás en modo {estado}.")

    def on_end(self):
        try:
            ride = self.session.end_ride()
            self.status_label.config(text=f"Carrera finalizada. Total: {ride.format_total()} €")
        except NoActiveRideError:
            self.status_label.config(text="No hay una carrera en curso. Inicie una carrera primero.")

    def refresh(self):
        if not self.root.winfo_exists():
            return

        if self.session.has_active_ride:
            ride = self.session.current_ride
            self.amount_label.config(text=f"{ride.get_total():.2f} €")
            if ride.state == "moving":
                self.banner.config(text="● EN MOVIMIENTO", bg=COLOR_MOVING)
            else:
                self.banner.config(text="● PARADO", bg=COLOR_STOPPED)
        else:
            self.amount_label.config(text="0.00 €")
            self.banner.config(text="SIN CARRERA ACTIVA", bg=COLOR_NO_RIDE)

        self.root.after(REFRESH_MS, self.refresh)


def main():
    rates = load_rates()
    session = RideSession(rates, FileStorage())
    root = tk.Tk()
    TaximetroGUI(root, session)
    root.mainloop()


if __name__ == "__main__":
    main()
