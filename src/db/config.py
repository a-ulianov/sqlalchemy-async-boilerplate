import math
import os

from dotenv import load_dotenv

load_dotenv()

class Config:
    """
    Configuration class for managing database connections using SQLAlchemy[async].

    Designed to be passed to the `Database.from_obj()` method.
    Supports two ways to specify connection parameters:
    1. Through a DSN string (`url` attribute)
    2. Through separate connection components

    Attributes
    ----------
    url : str, optional
        Connection DSN string (e.g.:
        'postgresql+asyncpg://user:password@host:port/database')

    driver : str, optional
        Connection driver (e.g.: 'postgresql+asyncpg')
        Required when `url` is not provided

    user : str, optional
        Database username. Required when `url` is not provided

    password : str, optional
        Database password. Required when `url` is not provided

    host : str, optional
        Database host. Required when `url` is not provided

    database : str, optional
        Database name. Required when `url` is not provided

    port : int, optional
        Database port (defaults to DBMS standard port)

    base : Type[DeclarativeBase], optional
        Base class for declarative models

    echo : bool, default=False
        SQL query logging

    pool_size : int, optional
        Connection pool size (recommended: cpu_cores * 2)

    max_overflow : int, optional
        Maximum number of connections beyond the pool size
        (recommended: pool_size / 2)

    isolation_level : str, default='REPEATABLE READ'
        Transaction isolation level:
        - 'READ UNCOMMITTED'
        - 'READ COMMITTED'
        - 'REPEATABLE READ'
        - 'SERIALIZABLE'

    **kwargs : Any
        Additional parameters for `create_async_engine`

    Notes
    -----
    Required parameters when `url` is not provided:
    - `driver`
    - `user`
    - `password`
    - `host`
    - `database`

    Example
    -------
    >>> from src.db import Database
    >>> db = Database.from_obj(Config)
    """

    # DSN parameters
    driver = 'postgresql+asyncpg'
    user = os.getenv('DB_USER')
    password = os.getenv('DB_PASS')
    host = os.getenv('DB_HOST')
    port = os.getenv('DB_PORT')
    database = os.getenv('DB_NAME')

    # Connection and session parameters
    echo = False
    pool_size = (os.cpu_count() or 1) * 2
    max_overflow = int(math.ceil(pool_size / 2))
    isolation_level = 'REPEATABLE READ'