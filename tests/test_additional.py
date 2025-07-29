import pytest
from unittest.mock import patch
from sqlalchemy.ext.asyncio import AsyncSession, AsyncConnection, async_sessionmaker
from src.db import Database
from src.db.config import Config


@pytest.mark.asyncio
async def test_session_generator():
    """Test that session() returns an async generator."""
    db = Database.from_obj(Config)

    gen = db.session()
    # Check the type
    assert hasattr(gen, '__aiter__')

    # Test generator functionality
    async for session in gen:
        assert isinstance(session, AsyncSession)
        break


@pytest.mark.asyncio
async def test_base_name():
    """Test that base_name property returns the correct value."""
    db = Database.from_obj(Config)

    assert db.base_name == Config.database


@pytest.mark.asyncio
async def test_connection_type():
    """Test the connection generator and its return type."""
    db = Database.from_obj(Config)

    gen = db.connection()

    # Check the type
    assert hasattr(gen, '__aiter__')

    # Test generator functionality
    async for conn in gen:
        assert isinstance(conn, AsyncConnection)
        break


@pytest.mark.asyncio
async def test_session_factory_type():
    """Test that session_factory has the correct type."""
    db = Database.from_obj(Config)

    assert isinstance(db.session_factory, async_sessionmaker)


@pytest.mark.asyncio
async def test_session_manager_rollback_on_exception():
    """Test rollback behavior when an exception occurs."""
    db = Database.from_obj(Config)

    class DummySession:
        def __init__(self):
            self.committed = False
            self.rolled_back = False
            self.closed = False

        def execute(self, stmt) -> None:
            # Dummy method for a testing
            ...

        def commit(self) -> None:
            # Dummy method for a testing
            self.committed = True

        def rollback(self) -> None:
            # Dummy method for a testing
            self.rolled_back = True

        def close(self) -> None:
            # Dummy method for a testing
            self.closed = True

    dummy_session = DummySession()

    with patch.object(db, '_session_factory', return_value=dummy_session):
        with pytest.raises(Exception):
            async with db.session_manager():
                # Raise an exception
                raise RuntimeError("Test exception")
        # Verify rollback was called
        assert dummy_session.rolled_back
        # Verify session was closed
        assert dummy_session.closed