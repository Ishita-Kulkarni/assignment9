# Test Configuration

This directory contains all test files for the FastAPI Calculator application.

## Test Structure

### Unit Tests (`test_operations.py`)
Tests individual functions in `operations.py`:
- Addition, subtraction, multiplication, and division functions
- Error handling (division by zero, invalid operations)
- Edge cases (large numbers, decimals, negative numbers, etc.)

### Integration Tests (`test_main.py`)
Tests API endpoints in `main.py`:
- All HTTP endpoints (/, /calculate, /health)
- Request/response validation
- Error handling and status codes
- Input validation with various data types

### End-to-End Tests (`test_e2e.py`)
Tests complete user workflows using Playwright:
- Swagger UI interactions
- API calls through browser
- Multiple sequential operations
- Concurrent requests
- Real-world user scenarios

## Running Tests

### Install Test Dependencies
```bash
pip install -r requirements-test.txt
playwright install chromium
```

### Run All Tests
```bash
pytest
```

### Run Specific Test Categories
```bash
# Unit tests only
pytest tests/test_operations.py

# Integration tests only
pytest tests/test_main.py

# E2E tests only
pytest tests/test_e2e.py
```

### Run with Coverage Report
```bash
pytest --cov=. --cov-report=html
```

### Run with Verbose Output
```bash
pytest -v
```

### Run Specific Test
```bash
pytest tests/test_operations.py::TestAddition::test_add_positive_numbers
```

## Test Markers

Tests can be marked with custom markers:
```bash
# Run only unit tests
pytest -m unit

# Run only integration tests
pytest -m integration

# Run only e2e tests
pytest -m e2e
```

## Coverage Reports

After running tests with coverage, view the HTML report:
```bash
# Generate coverage report
pytest --cov=. --cov-report=html

# Open the report
open htmlcov/index.html  # On macOS
xdg-open htmlcov/index.html  # On Linux
```

## Continuous Integration

These tests are designed to run in CI/CD pipelines. The E2E tests use headless browser mode by default.

## Test Data

Tests use inline test data for simplicity. For more complex scenarios, consider:
- Creating fixtures in `conftest.py`
- Using parametrized tests with `@pytest.mark.parametrize`
- Storing test data in separate JSON files
