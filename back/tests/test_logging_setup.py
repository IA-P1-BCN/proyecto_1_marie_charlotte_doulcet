import logging
import os
import re
import tempfile
import unittest

from taximetro.infrastructure.logging_setup import configure_logging


class TestConfigureLogging(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.log_file = os.path.join(self.temp_dir.name, "test_taximetro.log")

    def tearDown(self):
        for handler in logging.getLogger().handlers:
            handler.close()
        logging.getLogger().handlers.clear()
        self.temp_dir.cleanup()

    def test_adds_a_single_file_handler_at_info_level(self):
        logger = configure_logging(self.log_file)

        file_handlers = [h for h in logger.handlers if isinstance(h, logging.FileHandler)]
        self.assertEqual(len(file_handlers), 1)
        self.assertEqual(file_handlers[0].baseFilename, os.path.abspath(self.log_file))
        self.assertEqual(logger.level, logging.INFO)

    def test_calling_twice_does_not_duplicate_handlers(self):
        configure_logging(self.log_file)
        logger = configure_logging(self.log_file)

        self.assertEqual(len(logger.handlers), 1)

    def test_writes_timestamp_level_and_message_to_file(self):
        configure_logging(self.log_file)
        logging.info("hello %s", "world")

        with open(self.log_file) as f:
            content = f.read()
        self.assertRegex(content, r"^\d{4}-\d{2}-\d{2} [\d:,]+ INFO hello world\n$")
