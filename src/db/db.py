"""
Classes, interfaces, and tools for database interaction using SQLAlchemy async.
"""

import contextlib
from typing import AsyncGenerator, Optional, Type, AsyncIterator, Any

from sqlalchemy import MetaData, text, URL
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
    AsyncEngine, AsyncConnection,
)
from sqlalchemy.orm import DeclarativeBase

from .logger import Logger


class Database:
    """
    Class for managing asynchronous database interactions.

    Encapsulates engine and session factory creation.
    Provides context managers and other methods for working with connections and sessions.

    Args:
        url: Connection DSN string
        base: Base class for models (optional)
        echo: SQL query logging
        pool_size: Connection pool size
        max_overflow: Maximum number of connections beyond the pool size
        isolation_level: Transaction isolation level
        **kwargs: Additional parameters for logger configuration
    """
    def __init__(
        self,
        url: str,
        base: Optional[Type[DeclarativeBase]] = None,
        echo: bool = False,
        pool_size: int = 5,
        max_overflow: int = 10,
        isolation_level: str = 'REPEATABLE READ',
        **kwargs,
    ) -> None:
        self._url = url
        self._base = base or DeclarativeBase
        self._engine: AsyncEngine = create_async_engine(
            url,
            echo=echo,
            pool_size=pool_size,
            max_overflow=max_overflow,
            isolation_level=isolation_level,
            future=True,
        )

        self._session_factory: async_sessionmaker[AsyncSession] = async_sessionmaker(
            bind=self._engine,
            autoflush=False,
            expire_on_commit=False,
            class_=AsyncSession,
        )

        self.logging = Logger(**kwargs)
        self.logger = self.logging.logger

    @classmethod
    def from_obj(cls, obj: Any) -> 'Database':
        """
        Create a Database instance from a configuration object.

        Supports two ways to specify DSN:
        1. Directly via the `url` attribute.
        2. Via separate connection components (driver, user, password, host, port (optional), database).

        Also extracts all object attributes that match constructor parameters.

        Args:
            obj: Configuration object with connection parameters.

        Returns:
            Database: Database class instance.

        Raises:
            TypeError: When required attributes for DSN formation are missing.
        """
        dsn_required = ['driver', 'user', 'password', 'host', 'database']

        attrs: dict[str, Any] = {}

        # Form DSN
        if hasattr(obj, 'url') and obj.url is not None:
            attrs['url'] = obj.url
        else:
            missing = [attr for attr in dsn_required if not hasattr(obj, attr)]
            if missing:
                raise TypeError(f'Missing attributes: {missing}')

            # Form DSN with separate port specification
            dsn_args = {
                'drivername': obj.driver,
                'username': obj.user,
                'password': obj.password,
                'host': obj.host,
                'database': obj.database
            }
            if hasattr(obj, 'port'):
                dsn_args['port'] = obj.port
                dsn_required.append('port')
            attrs['url'] = URL.create(**dsn_args)

        # Collect additional parameters
        for attr_name in dir(obj):
            # Exclude methods and private attributes
            if attr_name.startswith('__') or callable(getattr(obj, attr_name)):
                continue

            # Skip already processed attributes
            if attr_name in attrs or attr_name in dsn_required:
                continue

            attrs[attr_name] = getattr(obj, attr_name)

        return cls(**attrs)

    @property
    def metadata(self) -> MetaData:
        """
        Access metadata of declared models.

        Returns:
            MetaData: Database metadata.
        """
        return self._base.metadata

    @property
    def session_factory(self) -> async_sessionmaker[AsyncSession]:
        """
        Factory for creating async sessions.

        Returns:
            async_sessionmaker[AsyncSession]: Session factory.
        """
        return self._session_factory

    @contextlib.asynccontextmanager
    async def session_manager(self) -> AsyncGenerator[AsyncSession, None]:
        """
        Async context manager for working with sessions.

        Guarantees automatic commit on success,
        rollback on exceptions, and proper session closure.

        Yields:
            AsyncSession: Async session for database operations
        """
        session = self._session_factory()
        try:
            yield session
            await session.commit()
        except Exception as e:
            # Rollback before re-raising exception
            await session.rollback()
            self.logger.debug(f"Session error: {e}")
            raise e
        finally:
            # Closure automatically rolls back unfinished transactions if no rollback occurred earlier
            await session.close()

    async def session(self) -> AsyncIterator[AsyncSession]:
        """
        Async generator returning an auto-closing session.

        Usage with FastAPI:
            session: AsyncSession = Depends(db.session)

        Returns:
            AsyncIterator[AsyncSession]: Session iterator.
        """
        async with self.session_manager() as session:
            yield session

    async def connection(self) -> AsyncIterator[AsyncConnection]:
        """
        Async generator for database connections to execute raw SQL without ORM.

        Usage:
            async with db.connection() as conn:
                result = await conn.execute(text("SELECT 1"))

        Returns:
            AsyncIterator[AsyncConnection]: Connection iterator.
        """
        try:
            async with self._engine.connect() as connection:
                yield connection
        except Exception as e:
            self.logger.debug('Error during connection context operations.\n', e)
            raise e

    async def check_connection(self) -> bool:
        """
        Check database availability.

        Returns:
            bool: True if connection successful, False otherwise.
        """
        try:
            async with self._engine.connect() as conn:
                await conn.execute(text('SELECT 1'))
            return True
        except Exception:
            return False

    async def _create_all_tables(self) -> None:
        """
        Create all tables declared in models.
        """
        async with self._engine.connect() as conn:
            await conn.run_sync(self.metadata.create_all)

    async def _drop_all_tables(self) -> None:
        """
        Drop all tables declared in models.
        """
        async with self._engine.connect() as conn:
            await conn.run_sync(self.metadata.drop_all)

    async def dispose(self) -> None:
        """
        Release connection resources, including connection pool.
        """
        await self._engine.dispose()

    @property
    def base_name(self) -> str:
        """
        Get database name.

        Returns:
            str: Database name.
        """
        return self._engine.url.database

    def __aenter__(self) -> 'Database':
        """Asynchronous context manager entry point."""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """Asynchronous context manager exit point"""
        await self.dispose()

    def __repr__(self) -> str:
        return f'Database(url="{self._url[:15]}...", base={self._base.__name__})'
