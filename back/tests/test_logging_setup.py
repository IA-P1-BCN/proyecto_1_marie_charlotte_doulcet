import unittest
import logging
import os
import tempfile

from taximetro.logging_setup import configure_logging

class TestConfigureLogging(unittest.TestCase):
    def setUp(self):
      self.temp_dir = tempfile.TemporaryDirectory()
      self.log_file = os.path.join(self.temp_dir.name, "test_taximetro.log")

    def tearDown(self):
      logging.getLogger().handlers.clear()

    def test_configure_logging_adds_file_handler_at_info_level(self):
      logger = configure_logging(self.log_file)

      file_handlers = [h for h in logger.handlers if isinstance(h, logging.FileHandler)]
      self.assertEqual(len(file_handlers), 1)
      self.assertEqual(file_handlers[0].baseFilename, os.path.abspath(self.log_file))
      self.assertEqual(logger.level, logging.INFO)

    def test_configure_logging_writes_timestamp_level_and_message_to_file(self):
      configure_logging(self.log_file)
      configure_logging(self.log_file)

      logger = logging.getLogger()
      file_handlers = [h for h in logger.handlers if isinstance(h, logging.FileHandler)]
      self.assertEqual(len(file_handlers), 1)
