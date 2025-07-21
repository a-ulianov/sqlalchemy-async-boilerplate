import pytest

from src.db import Database
from src.db.config import Config


@pytest.mark.asyncio
async def test_connection():
    """
    Test database connection.

    Verifies successful database connection through the Database class.
    Checks that:
    - Database instance is successfully created from configuration class
    - check_connection() method returns True when connection is successful

    Raises
    ------
    AssertionError
        If database connection fails

    Notes
    -----
    Test requirements:
    - Database server must be available with Config parameters
    - Valid credentials in Config
    - Required dependencies installed (async DB driver/sqlalchemy)

    Example
    -------
    >>> pytest test_connection.py
    """

    # Create database instance
    db = Database.from_obj(Config)

    # Test connection
    connected = await db.check_connection()
    assert connected, 'Failed to connect to database'