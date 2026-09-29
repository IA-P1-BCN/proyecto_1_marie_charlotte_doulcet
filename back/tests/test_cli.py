import unittest
from taximetro.application.auth_service import AuthService
from taximetro.application.ride_service import RideService
from taximetro.application.token_store import TokenStore
from taximetro.cli import TaximeterCli
from taximetro.domain.account import Account
from taximetro.domain.rates import Rates
from tests.fakes import FakePasswordHasher, InMemoryAccountRepository, InMemoryRatesRepository, InMemoryRideRepository


def make_cli(inputs=(), secrets=(), account=None):
    """Build a CLI wired to in-memory fakes; scripted keyboard input, captured output."""
    typed, hidden, output = iter(inputs), iter(secrets), []
    rates_repository = InMemoryRatesRepository(Rates(stopped_rate=0.02, moving_rate=0.05))
    rides = RideService(rates_repository, InMemoryRideRepository())
    auth = AuthService(InMemoryAccountRepository(account), FakePasswordHasher(), TokenStore())
    cli = TaximeterCli(
        rides, auth,
        read=lambda prompt="": next(typed),
        read_secret=lambda prompt="": next(hidden),
        write=output.append,
    )
    return cli, rides, auth, rates_repository, output


REGISTERED = Account(company="", password_hash="fake$secreto123")


class TestCliPassword(unittest.TestCase):
    def test_first_run_sets_up_the_password(self):
        cli, _, auth, _, _ = make_cli(secrets=["secreto123", "secreto123"])
        self.assertTrue(cli.require_password())
        self.assertTrue(auth.verify_password("secreto123"))

    def test_first_run_retries_on_mismatched_confirmation(self):
        cli, _, auth, _, output = make_cli(secrets=["secreto123", "wrong", "secreto123", "secreto123"])
        self.assertTrue(cli.require_password())
        self.assertTrue(any("no coinciden" in line for line in output))
        self.assertTrue(auth.verify_password("secreto123"))

    def test_first_run_rejects_an_empty_password(self):
        cli, _, auth, _, output = make_cli(secrets=["  ", "secreto123", "secreto123"])
        self.assertTrue(cli.require_password())
        self.assertTrue(any("vacía" in line for line in output))

    def test_wrong_then_correct_password_succeeds(self):
        cli, _, _, _, output = make_cli(secrets=["wrong", "secreto123"], account=REGISTERED)
        self.assertTrue(cli.require_password())
        self.assertTrue(any("incorrecta" in line for line in output))

    def test_q_at_the_password_prompt_exits(self):
        cli, _, _, _, output = make_cli(secrets=["q"], account=REGISTERED)
        self.assertFalse(cli.require_password())
        self.assertTrue(any("Saliendo" in line for line in output))

    def test_malformed_stored_hash_restarts_the_setup(self):
        cli, _, auth, _, output = make_cli(
            secrets=["nueva", "nueva"], account=Account(company="", password_hash="garbage")
        )
        self.assertTrue(cli.require_password())
        self.assertTrue(any("dañada" in line for line in output))
        self.assertTrue(auth.verify_password("nueva"))


class TestCliCommands(unittest.TestCase):
    def run_commands(self, commands):
        cli, rides, _, rates_repository, output = make_cli(inputs=commands)
        cli.command_loop()
        return "\n".join(output), rides, rates_repository

    def test_f_without_active_ride_prints_warning(self):
        text, _, _ = self.run_commands(["F", "Q"])
        self.assertIn("No hay una carrera en curso", text)

    def test_p_when_already_stopped_shows_already_in_state_message(self):
        text, _, _ = self.run_commands(["N", "P", "F", "Q"])
        self.assertIn("Ya estás en modo parado", text)

    def test_m_when_already_moving_shows_already_in_state_message(self):
        text, _, _ = self.run_commands(["N", "M", "M", "F", "Q"])
        self.assertIn("Ya estás en modo movimiento", text)

    def test_n_twice_says_a_ride_is_already_running(self):
        text, _, _ = self.run_commands(["N", "N", "F", "Q"])
        self.assertIn("Ya hay una carrera en curso", text)

    def test_full_ride_prints_the_total_and_shows_up_in_today_history(self):
        text, rides, _ = self.run_commands(["N", "M", "F", "H", "Q"])
        self.assertIn("Carrera finalizada. Total a pagar: 0.00 €", text)
        self.assertIn("Historial de carreras de hoy:", text)
        self.assertEqual(len(rides.get_today_history()), 1)

    def test_h_with_no_rides_says_so(self):
        text, _, _ = self.run_commands(["H", "Q"])
        self.assertIn("No hay carreras registradas para hoy.", text)

    def test_q_with_an_active_ride_is_refused(self):
        text, rides, _ = self.run_commands(["N", "Q", "F", "Q"])
        self.assertIn("Finalice carrera antes de salir", text)
        self.assertFalse(rides.has_active_ride)

    def test_t_changes_a_rate_and_persists_it(self):
        text, rides, rates_repository = self.run_commands(["T", "M", "0.1", "Q"])
        self.assertIn("Tarifa actualizada", text)
        self.assertEqual(rides.rates.moving_rate, 0.1)
        self.assertEqual(rates_repository.saved[-1].moving_rate, 0.1)

    def test_t_with_an_invalid_value_keeps_the_current_rate(self):
        for bad in ("abc", "-1", "0"):
            with self.subTest(bad=bad):
                text, rides, _ = self.run_commands(["T", "P", bad, "Q"])
                self.assertIn("Valor no válido", text)
                self.assertEqual(rides.rates.stopped_rate, 0.02)

    def test_t_with_an_unknown_rate_choice_is_rejected(self):
        text, _, _ = self.run_commands(["T", "X", "Q"])
        self.assertIn("Opción no válida", text)

    def test_unknown_command_is_reported(self):
        text, _, _ = self.run_commands(["Z", "Q"])
        self.assertIn("Comando no reconocido", text)


if __name__ == "__main__":
    unittest.main()
