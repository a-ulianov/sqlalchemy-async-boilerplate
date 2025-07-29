"""Logger configuration and initialization module.

This module provides a Logger class for configuring and initializing
a customizable logger with both console and file output capabilities.
"""

import logging
import os
from logging.handlers import QueueHandler, QueueListener
from queue import Queue


class Logger:
    """A customizable logger class with console and file output support.

    This class simplifies logger configuration by providing sensible defaults
    while allowing customization of logging levels, output destinations,
    and log message formatting.

    Args:
        logger_name (str, optional): Name of the logger instance.
            Defaults to 'undetected_chrome_driver'.
        logging_level (int, optional): Logging level (e.g., logging.INFO).
            Defaults to logging.INFO.
        log_to_file (bool, optional): Enable file logging if True.
            Defaults to False.
        logs_dir (str, optional): Directory for log files.
            Defaults to 'logs'.
        log_file (str, optional): Name of the log file.
            Defaults to 'undetected_chrome_driver.log'.
        **kwargs: Additional keyword arguments (currently unused).

    Raises:
        ValueError: If invalid file logging parameters are provided.
    """

    def __init__(
            self,
            logger_name: str = 'sa.manager',
            logging_level: int = logging.INFO,
            log_to_file: bool = False,
            logs_dir: str = 'logs',
            log_file: str = 'sa-manager.log',
            **kwargs,
    ):
        """Initialize the logger with specified configuration."""
        self.logger: logging.Logger = logging.getLogger(name=logger_name)
        self.logger.setLevel(logging_level)

        self.logger.propagate = False

        self._listener = None
        handlers = []

        # Create formatter with timestamp, logger name, level and message
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )

        handlers.append(
            self._get_console_handler(formatter, logging_level)
        )

        # Configure file handler if file logging is enabled
        if log_to_file:
            handlers.append(
                self._get_file_handler(
                    logs_dir,
                    log_file,
                    formatter,
                    logging_level
                )
            )

        self._configure_queue_handler(handlers)

    def _configure_queue_handler(self, handlers: list[logging.Handler]) -> None:
        """Create async handler"""
        queue = Queue(maxsize=1000)
        handler = QueueHandler(queue)

        self._listener = QueueListener(queue, *handlers)

        self.logger.addHandler(handler)
        self._listener.start()

    @staticmethod
    def _get_console_handler(formatter: logging.Formatter, logging_level: int) -> logging.StreamHandler:
        """Create, configure and return console handler"""
        handler = logging.StreamHandler()
        handler.setLevel(logging_level)
        handler.setFormatter(formatter)

        return handler

    @staticmethod
    def _get_file_handler(logs_dir: str,
                          log_file: str,
                          formatter: logging.Formatter,
                          logging_level: int
                          ) -> logging.FileHandler:
        """Create, configure and return file handler"""
        # Validate file logging parameters
        if not isinstance(logs_dir, str) or not isinstance(log_file, str) or not log_file.strip():
            raise ValueError(
                'Check log file name and path to logs directory are correct.'
            )

        # Ensure logs directory exists
        os.makedirs(logs_dir, exist_ok=True)

        # Create and configure file handler
        handler = logging.FileHandler(
            os.path.join(logs_dir, log_file)
        )
        handler.setLevel(logging_level)
        handler.setFormatter(formatter)

        return handler

    def _cleanup_logger(self) -> None:
        """Safely remove all logger components."""
        for handler in self.logger.handlers[:]:
            self.logger.removeHandler(handler)
            handler.close()
        self.logger.filters.clear()

    def shutdown(self) -> None:
        """Clean up logging resources."""
        self._cleanup_logger()

        if self._listener is not None:
            self._listener.stop()
            self._listener = None

    def __enter__(self) -> 'Logger':
        """Context manager realisation"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Completion of work of context manager with correct resources cleaning"""
        self.shutdown()

    def __del__(self) -> None:
        """Clean up logging resources."""
        self.shutdown()