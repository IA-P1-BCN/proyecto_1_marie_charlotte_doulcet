import unittest
from taximetro.cli import main, require_password
import io
from contextlib import redirect_stdout
from unittest.mock import patch
from datetime import date

class TestCliLoop(unittest.TestCase):

    @patch("taximetro.cli.save_password_hash")
    @patch("taximetro.cli.hash_password", return_value="salt$digest")
    @patch("taximetro.cli.getpass.getpass", return_value="secreto123")
    @patch("taximetro.cli.is_password_set", return_value=False)
    def test_require_password_first_run_sets_up_password(self, mock_is_set, mock_getpass, mock_hash, mock_save):
        require_password()
        mock_hash.assert_called_once_with("secreto123")
        mock_save.assert_called_once_with("salt$digest")

    @patch("taximetro.cli.check_password", side_effect=[False, True])
    @patch("taximetro.cli.load_password_hash", return_value="salt$digest")
    @patch("taximetro.cli.is_password_set", return_value=True)
    @patch("taximetro.cli.getpass.getpass", side_effect=["wrong", "secreto123"])
    def test_require_password_wrong_then_correct_password_succeeds(self, mock_getpass, mock_is_set, mock_load, mock_check):
        require_password()
        self.assertEqual(mock_check.call_count, 2)

    @patch("taximetro.cli.require_password", return_value=None)
    @patch("builtins.input", side_effect=["F", "Q"])
    def test_f_without_active_ride_prints_warning(self, mock_input, mock_require_password):
        output = io.StringIO()
        with redirect_stdout(output):
            try:
                main()
            except StopIteration:
                pass
        self.assertIn("No hay una carrera en curso", output.getvalue())

    @patch("taximetro.cli.save_password_hash")
    @patch("taximetro.cli.hash_password", return_value="salt$digest")
    @patch("taximetro.cli.getpass.getpass", side_effect=["secreto123", "wrong", "secreto123", "secreto123"])
    @patch("taximetro.cli.is_password_set", return_value=False)
    def test_require_password_first_run_retries_on_mismatched_confirmation(self, mock_is_set, mock_getpass, mock_hash, mock_save):
        output = io.StringIO()
        with redirect_stdout(output):
            require_password()
        self.assertIn("no coinciden", output.getvalue())
        mock_hash.assert_called_once_with("secreto123")
        mock_save.assert_called_once_with("salt$digest")
    @patch("taximetro.cli.require_password", return_value=None)
    @patch("builtins.input", side_effect=["N", "P", "Q"])
    def test_p_when_already_stopped_shows_already_in_state_message(self, mock_input, mock_require_password):
        output = io.StringIO()
        with redirect_stdout(output):
            try:
                main()
            except StopIteration:
                pass
        self.assertIn("Ya estás en modo parado", output.getvalue())

    @patch("taximetro.cli.require_password", return_value=None)
    @patch("builtins.input", side_effect=["N", "M", "M", "Q"])
    def test_m_when_already_moving_shows_already_in_state_message(self, mock_input, mock_require_password):
        output = io.StringIO()
        with redirect_stdout(output):
            try:
                main()
            except StopIteration:
                pass
        self.assertIn("Ya estás en modo movimiento", output.getvalue())

if __name__ == '__main__':
    unittest.main()