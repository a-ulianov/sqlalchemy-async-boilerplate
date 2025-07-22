import logging
import math
import os
from typing import Optional, Type

from dotenv import load_dotenv
from sqlalchemy.orm import DeclarativeBase

load_dotenv()


class Config:
    """
    Configuration class for managing database connections using SQLAlchemy[async].

    This class provides centralized configuration for database connections with support for:
    - Connection via DSN string or separate components
    - Connection pooling settings
    - Transaction isolation levels
    - SQL query logging
    - Logger configuration

    Designed to be passed to the `Database.from_obj()` method. When url is not provided,
    separate connection components (driver, user, password, host, database) are required.

    Attributes:
        url (Optional[str]): Connection DSN string (e.g. 'postgresql+asyncpg://user:password@host:port/database').
        driver (str): Connection driver (e.g. 'postgresql+asyncpg'). Required when url is not provided.
        user (Optional[str]): Database username. Required when url is not provided.
        password (Optional[str]): Database password. Required when url is not provided.
        host (Optional[str]): Database host. Required when url is not provided.
        database (Optional[str]): Database name. Required when url is not provided.
        port (Optional[str]): Database port (defaults to DBMS standard port).
        base (Optional[Type[DeclarativeBase]]): Base class for declarative models.
        echo (bool): Flag to enable SQL query logging (default: False).
        pool_size (int): Connection pool size (recommended: cpu_cores * 2).
        max_overflow (int): Maximum connections beyond pool size (recommended: pool_size / 2).
        isolation_level (str): Transaction isolation level (default: 'REPEATABLE READ').
        logger_name (str): Name identifier for the logger instance.
        logging_level (int): Default logging level (e.g., logging.INFO).
        log_to_file (bool): Enable file logging when True.
        logs_dir (str): Directory path for log file storage.
        log_file (str): Name of the log file.
    """

    # DSN parameters
    url: Optional[str] = None
    """Connection DSN string. Alternative to specifying individual connection components."""

    driver: str = 'postgresql+asyncpg'
    """Database driver (e.g. 'postgresql+asyncpg'). Required when url is not provided."""

    user: Optional[str] = os.getenv('DB_USER')
    """Database username. Required when url is not provided."""

    password: Optional[str] = os.getenv('DB_PASS')
    """Database password. Required when url is not provided."""

    host: Optional[str] = os.getenv('DB_HOST')
    """Database host. Required when url is not provided."""

    port: Optional[str] = os.getenv('DB_PORT')
    """Database port. Defaults to DBMS standard port if not specified."""

    database: Optional[str] = os.getenv('DB_NAME')
    """Database name. Required when url is not provided."""

    # SQLAlchemy configuration
    base: Optional[Type[DeclarativeBase]] = None
    """Base class for declarative models."""

    echo: bool = False
    """When True, enables SQL query logging."""

    pool_size: int = (os.cpu_count() or 1) * 2
    """Connection pool size (recommended: cpu_cores * 2)."""

    max_overflow: int = int(math.ceil(pool_size / 2))
    """Maximum number of connections beyond the pool size (recommended: pool_size / 2)."""

    isolation_level: str = 'REPEATABLE READ'
    """
    Transaction isolation level:
    - 'READ UNCOMMITTED'
    - 'READ COMMITTED'
    - 'REPEATABLE READ'
    - 'SERIALIZABLE'
    """

    # Logger configuration
    logger_name: str = 'sa.manager'
    """Default name for the logger instance."""

    logging_level: int = logging.INFO
    """Default logging level (INFO). Can be set to DEBUG for more verbose output."""

    log_to_file: bool = False
    """When True, enables logging to file in addition to console output."""

    logs_dir: str = 'logs'
    """Directory where log files will be stored if file logging is enabled."""

    log_file: str = 'sa-manager.log'
    """Default name for the log file if file logging is enabled."""