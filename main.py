import pytest
from pathlib import Path


def run_tests():
    """
    Run test suite for database operations.

    Configures and executes pytest with:
    - Verbose output
    - Automatic asyncio mode
    - Suppressed deprecation warnings

    Returns
    -------
    int
        pytest exit code (0 for success, 1 for failures)
    """
    test_path = str(Path(__file__).parent / 'tests')

    return pytest.main([
        test_path,
        '-v',
        '--asyncio-mode=auto',
        '-W', 'ignore::DeprecationWarning',
    ])


def main():
    """Main entry point for test execution."""

    exit_code = run_tests()

    if exit_code == 0:
        print('✅ All tests passed successfully!')
    else:
        print('❌ Some tests failed!')


if __name__ == '__main__':
    main()
