"""Tests for Logger class."""

import pytest
from src.db import Logger


class TestLogger:
    """Test class for verifying the functionality of the Logger class."""

    def test_default_initialization(self, capsys):
        """Verify default initialization creates a logger with console handler only."""
        logger_name = "test_default_logger"
        logger = Logger(logger_name=logger_name)
        test_message = "Test default logger message"

        logger.logger.info(test_message)
        logger.shutdown()  # Явный shutdown для обработки сообщений

        captured = capsys.readouterr()
        assert test_message in captured.err
        assert logger_name in captured.err

    def test_file_logging_initialization(self, tmp_path):
        """Verify file handler is added when log_to_file is enabled."""
        logs_dir = tmp_path / "logs"
        log_file = "test.log"
        logger = Logger(
            logger_name="test_file_logger",
            log_to_file=True,
            logs_dir=str(logs_dir),
            log_file=log_file
        )
        test_message = "Test file logger message"

        logger.logger.info(test_message)
        logger.shutdown()  # Явный shutdown для обработки сообщений

        log_path = logs_dir / log_file
        assert log_path.exists()

        with open(log_path) as f:
            log_content = f.read()
            assert test_message in log_content
            assert "INFO" in log_content

    def test_invalid_file_parameters(self):
        """Verify ValueError is raised for invalid file logging parameters."""
        with pytest.raises(ValueError):
            Logger(log_to_file=True, logs_dir=None, log_file="valid.log")

        with pytest.raises(ValueError):
            Logger(log_to_file=True, logs_dir="valid_dir", log_file="")

    def test_log_output_format(self, capsys):
        """Verify log messages use the correct format."""
        logger_name = "test_format_logger"
        logger = Logger(logger_name=logger_name)
        test_message = "Test log message"

        logger.logger.info(test_message)
        logger.shutdown()  # Явный shutdown для обработки сообщений

        captured = capsys.readouterr()
        log_output = captured.err.strip()

        assert logger_name in log_output
        assert test_message in log_output
        assert "INFO" in log_output
        # Проверяем формат: время - имя - уровень - сообщение
        assert log_output.startswith("20")  # Год
        assert " - " in log_output
        parts = log_output.split(" - ")
        assert len(parts) >= 4
        assert parts[1] == logger_name
        assert parts[2] == "INFO"
        assert parts[3] == test_message