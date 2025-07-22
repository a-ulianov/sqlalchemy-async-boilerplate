# SQLAlchemy Async Boilerplate

[![Tests](https://github.com/a-ulianov/sqlalchemy-async-boilerplate/actions/workflows/test.yaml/badge.svg)](https://github.com/a-ulianov/sqlalchemy-async-boilerplate/actions/workflows/test.yaml)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=a-ulianov_sqlalchemy-async-boilerplate&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=a-ulianov_sqlalchemy-async-boilerplate)[![codecov](https://codecov.io/gh/a-ulianov/sqlalchemy-async-boilerplate/branch/main/graph/badge.svg)](https://codecov.io/gh/a-ulianov/sqlalchemy-async-boilerplate)
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
   echo "DB_USER=your_user\nDB_PASS=your_password\nDB_HOST=localhost\nDB_PORT=5432\nDB_NAME=your_db" > .env
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
# Custom configuration with logger parameters
db = Database(
    url="postgresql+asyncpg://user:password@host:port/database",
    pool_size=20,
    max_overflow=10,
    isolation_level="READ COMMITTED",
    logger_name="custom.logger",
    log_to_file=True
)

# Access logger instance
db.logger.info("Database initialized")
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

#### Logger Integration

All logger parameters from Config are automatically passed to the Logger class:

```python
Database.from_obj(Config)  # Uses logger settings from Config
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
│       └── logger.py              # Logger class implementation
├── tests/
│   ├── test_connection.py         # Connection tests
│   ├── test_session_manager.py    # Session tests
│   ├── test_logger.py             # Logger tests
│   └── test_additional.py         # Additional tests
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
pytest -v --asyncio-mode=auto
```

## License

MIT License - see [LICENSE](LICENSE) for details.

## Acknowledgments

- SQLAlchemy team for the excellent ORM
- PostgreSQL for the powerful open-source database
- All contributors to asyncpg and related async ecosystem
