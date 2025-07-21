# SQLAlchemy Async Boilerplate

[![Tests](https://github.com/a-ulianov/sqlalchemy-async-boilerplate/actions/workflows/test.yaml/badge.svg)](https://github.com/a-ulianov/sqlalchemy-async-boilerplate/actions/workflows/test.yaml)
[![Python Version](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![SQLAlchemy Version](https://img.shields.io/badge/SQLAlchemy-2.0+-lightgrey.svg)](https://www.sqlalchemy.org/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

A modern, production-ready boilerplate for async database operations using SQLAlchemy 2.0+ with PostgreSQL (or other sql-db) support.

## Features

- 🚀 **Async-first** design using SQLAlchemy 2.0+ async API
- 🛠️ **Database class** with full session/connection management
- ⚙️ **Environment-based configuration** via `.env` files
- 📝 **Comprehensive logging** with configurable handlers
- ✅ **Full test coverage** including async session management
- 🐘 **PostgreSQL optimized** but easily adaptable to other databases
- 🔄 **Context managers** for automatic session/connection handling
- 🧪 **Pytest integration** with async test support

## Installation

### Prerequisites

- Python 3.11 or higher
- PostgreSQL 14+ (or compatible database)
- pip

### Install via pip

```bash
pip install git+https://github.com/a-ulianov/sqlalchemy-async-boilerplate.git
```

### Manual installation

1. Clone the repository:
   ```bash
   git clone https://github.com/a-ulianov/sqlalchemy-async-boilerplate.git
   cd sqlalchemy-async-boilerplate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create `.env` file:
   ```bash
   cp .env.example .env
   # Edit with your database credentials
   ```

## Usage

### Basic Usage

```python
from src.db import Database
from src.db.config import Config

# Initialize database
db = Database.from_obj(Config)

# Using session manager
async with db.session_manager() as session:
    result = await session.execute(text("SELECT 1"))
    print(result.scalar())  # Output: 1
```

### Advanced Usage

```python
# Custom configuration
from sqlalchemy.ext.asyncio import async_sessionmaker

db = Database(
    url="postgresql+asyncpg://user:password@host:port/database",
    pool_size=20,
    max_overflow=10,
    isolation_level="READ COMMITTED"
)

# Using as FastAPI dependency
async def get_db_session():
    async with db.session_manager() as session:
        yield session

# Raw connection access
async with db.connection() as conn:
    await conn.execute(text("CREATE TABLE IF NOT EXISTS test (id SERIAL PRIMARY KEY)"))
```

## API Documentation

### `Database` Class

#### Core Methods

| Method | Description |
|--------|-------------|
| `session_manager()` | Context manager for automatic session handling (commit/rollback) |
| `connection()` | Context manager for raw connection access |
| `check_connection()` | Verifies database availability |
| `session()` | Async generator for dependency injection (e.g., FastAPI) |

#### Configuration

Configure via `Config` class or direct parameters:

```python
Database(
    url="postgresql+asyncpg://...",  # DSN string
    pool_size=10,                   # Connection pool size
    max_overflow=5,                 # Additional connections
    isolation_level="REPEATABLE READ",
    echo=True                       # Enable SQL logging
)
```

## Project Structure

```
sqlalchemy-async-boilerplate/
├── .github/
│   └── workflows/
│       └── test.yml               # CI/CD pipeline
├── src/
│   ├── __init__.py
│   └── db/
│       ├── __init__.py            # Package exports
│       ├── db.py                  # Main Database class
│       ├── config.py              # Configuration loader
│       └── logger.py              # Logging setup
├── tests/
│   ├── test_connection.py         # Connection tests
│   └── test_session_manager.py    # Session tests
├── .env.example                   # Environment template
├── .gitignore
├── main.py                        # Test runner
├── pyproject.toml
├── README.md
└── requirements.txt
```

## Development

### Running Tests

```bash
# Run all tests
python main.py

# Or directly with pytest
pytest tests/ -v --asyncio-mode=auto
```

### CI/CD Pipeline

The GitHub Actions workflow (`.github/workflows/test.yml`) includes:
- PostgreSQL service container
- Python 3.11 environment
- Async test execution
- Dependency caching

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -am 'Add some feature'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Create a Pull Request

## License

MIT License - see [LICENSE](LICENSE) for details.

## Acknowledgments

- SQLAlchemy team for the excellent ORM
- PostgreSQL for the powerful open-source database
- All contributors to asyncpg and related async ecosystem
