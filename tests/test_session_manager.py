import pytest
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from src.db import Database
from src.db.config import Config


@pytest.mark.asyncio
async def test_session_manager():
    """
    Test the correct operation of the session_manager context manager.

    Verifies that:
    - The context manager returns a valid AsyncSession object
    - The session is available for use within the context

    Raises
    ------
    AssertionError
        If the session is not obtained or unavailable for operations
    """

    db = Database.from_obj(Config)

    async with db.session_manager() as session:
        # Basic session checks
        assert session is not None, 'Session was not returned'
        assert isinstance(session, AsyncSession), (
            f'Expected `AsyncSession`, got `{session.__class__.__name__}`.'
        )

        # Verify session is operational
        try:
            await session.execute(text('SELECT 1'))
        except Exception as e:
            pytest.fail(f'Session is not working: {str(e)}')