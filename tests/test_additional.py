import pytest
from unittest.mock import patch
from sqlalchemy.ext.asyncio import AsyncSession, AsyncConnection, async_sessionmaker
from src.db import Database
from src.db.config import Config


@pytest.mark.asyncio
async def test_session_generator():
    """
    Проверка, что session() возвращает асинхронный генератор.
    """
    db = Database.from_obj(Config)

    gen = db.session()
    # Проверка типа
    assert hasattr(gen, '__aiter__')

    # Проверка работы генератора
    async for session in gen:
        assert isinstance(session, AsyncSession)
        break

@pytest.mark.asyncio
async def test_base_name():
    """
    Проверка метода base_name возвращает правильное значение
    """
    db = Database.from_obj(Config)

    assert db.base_name == Config.database

@pytest.mark.asyncio
async def test_connection_type():
    """
    Проверка генератора connection и типа данных, возвращаемых генератором
    """
    db = Database.from_obj(Config)

    gen = db.connection()

    # Проверка типа
    assert hasattr(gen, '__aiter__')

    # Проверка работы генератора
    async for conn in gen:
        assert isinstance(conn, AsyncConnection)
        break

@pytest.mark.asyncio
async def test_session_factory_type():
    """
    Проверка соответствия типа данных фабрики сессий
    """
    db = Database.from_obj(Config)

    assert isinstance(db.session_factory, async_sessionmaker)

@pytest.mark.asyncio
async def test_session_manager_rollback_on_exception():
    """
    Проверка rollback при возникновении исключения.
    """
    db = Database.from_obj(Config)

    class DummySession:
        def __init__(self):
            self.committed = False
            self.rolled_back = False
            self.closed = False

        async def execute(self, stmt):
            pass

        async def commit(self):
            self.committed = True

        async def rollback(self):
            self.rolled_back = True

        async def close(self):
            self.closed = True

    dummy_session = DummySession()

    with patch.object(db, '_session_factory', return_value=dummy_session):
        with pytest.raises(Exception):
            async with db.session_manager() as session:
                # Возбуждаем исключение
                raise RuntimeError("Test exception")
        # Проверяем, что rollback вызван
        assert dummy_session.rolled_back
        # Проверяем, что сессия закрыта
        assert dummy_session.closed
