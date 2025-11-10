# Continuous Integration & Deployment

## Overview
The FastAPI Calculator project uses GitHub Actions for automated testing, code quality checks, security scanning, and deployment.

## Workflows

### 1. CI Workflow (`.github/workflows/ci.yml`)
**Triggers:** Push and Pull Request to `main` and `develop` branches

#### Features:
- **Multi-version Testing**: Tests against Python 3.9, 3.10, 3.11, and 3.12
- **Automated Testing**:
  - Unit tests (`test_operations.py`)
  - Integration tests (`test_main.py`)
  - Logging tests (`test_logging.py`)
  - Coverage reporting
  - **Note**: E2E tests are excluded from main CI (run separately or locally)
- **Code Linting**: Flake8 for syntax and style checks
- **Coverage Upload**: Automatic upload to Codecov
- **Artifacts**: Test results and logs saved for all Python versions
- **Build Verification**: Ensures application can start successfully

#### Matrix Testing:
```yaml
strategy:
  matrix:
    python-version: ['3.9', '3.10', '3.11', '3.12']
```

### 2. Code Quality Workflow (`.github/workflows/code-quality.yml`)
**Triggers:** Push, Pull Request, and Weekly Schedule

#### Features:
- **Code Formatting**: Black for consistent code style
- **Import Sorting**: isort for organized imports
- **Linting**: Flake8 and Pylint for code quality
- **Type Checking**: MyPy for static type analysis
- **Security Scanning**: Bandit for security vulnerabilities
- **Dependency Check**: Safety for known CVEs in dependencies
- **Dependency Review**: Automated review for pull requests

### 3. E2E Tests Workflow (`.github/workflows/e2e-tests.yml`)
**Triggers:** Manual dispatch and Weekly schedule

#### Features:
- **Optional E2E Testing**: Playwright-based browser tests
- **Separate Environment**: Ubuntu 22.04 for better compatibility
- **Manual Trigger**: Run on-demand via workflow_dispatch
- **Weekly Schedule**: Automated weekly checks

### 4. Deployment Workflow (`.github/workflows/deploy.yml`)
**Triggers:** Release publication and Manual dispatch

#### Features:
- **Pre-deployment Testing**: Full test suite before deployment
- **Build Package**: Creates deployment artifact
- **Environment Selection**: Choose staging or production
- **Artifact Upload**: Deployment package saved as artifact

## Workflow Status Badges

Add these badges to your README to show workflow status:

```markdown
![CI](https://github.com/Ishita-Kulkarni/assignment_8/workflows/FastAPI%20Calculator%20CI/badge.svg)
![Code Quality](https://github.com/Ishita-Kulkarni/assignment_8/workflows/Code%20Quality%20&%20Security/badge.svg)
```

## CI/CD Pipeline Flow

```
┌─────────────────┐
│   Code Push     │
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────────────┐
│         GitHub Actions Triggered        │
└────────┬────────────────────────────────┘
         │
         ├──────────────────────┬──────────────────────┐
         ▼                      ▼                      ▼
┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐
│   CI Workflow    │  │  Code Quality    │  │  Security Scan   │
│                  │  │                  │  │                  │
│ • Lint Code      │  │ • Black Format   │  │ • Bandit Scan    │
│ • Run Tests      │  │ • isort Check    │  │ • Safety Check   │
│ • Coverage       │  │ • Pylint         │  │ • Dependency     │
│ • Multi-version  │  │ • MyPy           │  │   Review         │
└────────┬─────────┘  └────────┬─────────┘  └────────┬─────────┘
         │                      │                      │
         └──────────────────────┴──────────────────────┘
                                │
                                ▼
                     ┌──────────────────────┐
                     │   All Checks Pass?   │
                     └──────────┬───────────┘
                                │
                    ┌───────────┴───────────┐
                    ▼                       ▼
            ┌──────────────┐        ┌──────────────┐
            │   Success    │        │    Failure   │
            │              │        │              │
            │ • Merge OK   │        │ • Fix Issues │
            │ • Deploy OK  │        │ • Re-push    │
            └──────────────┘        └──────────────┘
```

## Test Execution

### Unit Tests
```bash
pytest tests/test_operations.py -v --tb=short
```
- Tests all calculator operations
- 37 test cases
- 100% coverage on operations.py

### Integration Tests
```bash
pytest tests/test_main.py -v --tb=short
```
- Tests all API endpoints
- 37 test cases
- 100% coverage on main.py

### Logging Tests
```bash
pytest tests/test_logging.py -v --tb=short
```
- Tests logging functionality
- 26 test cases
- 100% coverage on logger_config.py

### Full Test Suite with Coverage
```bash
pytest tests/test_operations.py tests/test_main.py tests/test_logging.py -v \
  --cov=. --cov-report=xml --cov-report=term-missing
```

### E2E Tests (Run Locally or via Manual Workflow)
```bash
# Install Playwright browsers first
playwright install chromium

# Run E2E tests
pytest tests/test_e2e.py -v
```

**Note**: E2E tests are excluded from the main CI pipeline due to Playwright dependency complexity in CI environments. They can be:
- Run locally before pushing
- Triggered manually via GitHub Actions
- Run automatically on a weekly schedule

## Code Quality Checks

### Flake8 (Linting)
```bash
flake8 . --count --statistics --exclude=venv,htmlcov,.pytest_cache
```
- Checks Python code style
- Enforces PEP 8 guidelines
- Detects syntax errors

### Black (Formatting)
```bash
black --check --diff . --exclude='venv/|htmlcov/|\.pytest_cache/'
```
- Ensures consistent code formatting
- PEP 8 compliant

### isort (Import Sorting)
```bash
isort --check-only --diff . --skip venv
```
- Organizes imports
- Consistent import structure

### Pylint (Static Analysis)
```bash
pylint *.py --disable=C0111,R0903
```
- Advanced code analysis
- Detects code smells
- Suggests improvements

### MyPy (Type Checking)
```bash
mypy . --ignore-missing-imports --exclude venv
```
- Static type checking
- Ensures type safety

### Bandit (Security)
```bash
bandit -r . --exclude ./venv
```
- Scans for security issues
- Detects common vulnerabilities

### Safety (Dependency Scan)
```bash
safety check
```
- Checks dependencies for known vulnerabilities
- Reports CVEs

## Artifacts

### Test Results
- Location: `htmlcov/`, `.coverage`, `coverage.xml`
- Retention: 90 days
- Contains: Coverage reports, test results

### Logs
- Location: `logs/`
- Retention: 90 days
- Contains: Application logs from test runs

### Security Reports
- Location: `bandit-report.json`
- Retention: 90 days
- Contains: Security scan results

### Deployment Package
- Location: `fastapi-calculator.tar.gz`
- Retention: 90 days
- Contains: Deployment-ready application

## Local CI Testing

### Run CI checks locally before pushing:

```bash
# Install CI dependencies
pip install flake8 pylint mypy black isort bandit safety

# Run linting
flake8 . --exclude=venv,htmlcov,.pytest_cache

# Run tests
pytest tests/test_operations.py tests/test_main.py tests/test_logging.py -v

# Check formatting
black --check .

# Check imports
isort --check-only .

# Security scan
bandit -r . --exclude ./venv

# Dependency check
safety check
```

## Troubleshooting

### Tests Failing in CI but Passing Locally
1. Check Python version differences
2. Verify dependencies are installed
3. Check for OS-specific issues
4. Review environment variables

### Playwright Browser Installation Issues
- Ensure `playwright install chromium` is run
- Run `playwright install-deps` for system dependencies

### Coverage Upload Failures
- Non-critical, doesn't fail the build
- Check Codecov token if needed

### Flake8 Warnings
- Fix code style issues
- Update `.flake8` config if needed

## Configuration Files

### `.flake8` (Optional)
Create to customize linting:
```ini
[flake8]
max-line-length = 127
exclude = venv,htmlcov,.pytest_cache
ignore = E203,W503
```

### `pyproject.toml`
Already configured with pytest settings

## Environment Variables

### Secrets (Configure in GitHub Settings)
- `CODECOV_TOKEN`: For coverage uploads (optional)
- `DEPLOY_KEY`: For deployment (if needed)

### Variables
- `PYTHON_VERSION`: Default Python version
- `LOG_LEVEL`: Logging level for CI

## Best Practices

### Before Committing:
1. ✅ Run tests locally
2. ✅ Check code formatting
3. ✅ Run linting
4. ✅ Review changes
5. ✅ Update documentation

### Pull Request Workflow:
1. Create feature branch
2. Make changes
3. Run local CI checks
4. Push to GitHub
5. Wait for CI to pass
6. Request review
7. Merge when approved

### Release Workflow:
1. Ensure all tests pass
2. Update version number
3. Create release tag
4. GitHub Actions triggers deployment
5. Verify deployment

## Monitoring

### Check Workflow Status:
- Visit: `https://github.com/Ishita-Kulkarni/assignment_8/actions`
- View: Workflow runs, logs, and artifacts
- Download: Test results and coverage reports

### Email Notifications:
- Automatic for workflow failures
- Configurable in GitHub settings

## Performance

### Typical CI Run Times:
- **Lint**: ~30 seconds
- **Unit Tests**: ~1-2 seconds
- **Integration Tests**: ~1-2 seconds
- **Logging Tests**: ~1-2 seconds
- **Full Suite**: ~2-3 minutes per Python version
- **Total (all versions)**: ~8-12 minutes

### Optimization Tips:
- Cache pip dependencies (already configured)
- Run tests in parallel (matrix strategy)
- Skip E2E tests in CI (optional)

## Future Enhancements

### Potential Additions:
- [ ] Docker build and push
- [ ] Deploy to cloud (AWS, Azure, GCP)
- [ ] Performance testing
- [ ] Load testing
- [ ] API documentation generation
- [ ] Changelog automation
- [ ] Semantic release

## Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Python Package Index](https://pypi.org/)
- [Codecov](https://codecov.io/)
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)

## Summary

The CI/CD pipeline ensures:
✅ Code quality and consistency
✅ Automated testing on multiple Python versions
✅ Security vulnerability detection
✅ Coverage tracking
✅ Easy deployment process
✅ Fast feedback on code changes
