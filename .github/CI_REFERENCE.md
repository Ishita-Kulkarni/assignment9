# CI Workflow Quick Reference

## Workflows Overview

### 1. Main CI Pipeline ✅
**File**: `.github/workflows/ci.yml`  
**Status**: Active on every push/PR  
**Tests**: Unit + Integration + Logging (100 tests)

### 2. Code Quality ✅
**File**: `.github/workflows/code-quality.yml`  
**Status**: Active on every push/PR  
**Checks**: Linting, formatting, security

### 3. E2E Tests (Optional) 🔄
**File**: `.github/workflows/e2e-tests.yml`  
**Status**: Manual or weekly  
**Tests**: Browser-based E2E tests

### 4. Deployment 🚀
**File**: `.github/workflows/deploy.yml`  
**Status**: On release/manual  
**Action**: Build and deploy

## Why E2E Tests are Separate

E2E tests using Playwright require browser binaries and system dependencies that can be complex to install in CI environments, especially on newer Ubuntu versions. To ensure:

1. ✅ Fast CI feedback (tests complete in ~2-3 minutes)
2. ✅ Reliable builds (no dependency installation failures)
3. ✅ Core functionality always tested (100 unit/integration/logging tests)
4. ✅ E2E tests still available (run locally or manually)

## Running E2E Tests

### Locally
```bash
# Install browser
playwright install chromium

# Run tests
pytest tests/test_e2e.py -v
```

### In GitHub Actions
1. Go to Actions tab
2. Select "E2E Tests (Optional)"
3. Click "Run workflow"
4. Choose branch and run

### Scheduled
E2E tests run automatically every Sunday at midnight.

## Test Count by Pipeline

```
Main CI:
├─ Unit Tests: 37
├─ Integration Tests: 37
├─ Logging Tests: 26
└─ Total: 100 tests ✅

E2E (Optional):
└─ Browser Tests: 13+ test classes
```

## CI Failure Troubleshooting

### If Main CI Fails
1. Check the Actions tab for error details
2. Run `./ci_check.sh` locally to reproduce
3. Fix the issue
4. Push again

### If E2E Tests Fail
- Non-critical - doesn't block merges
- Check if tests pass locally
- May indicate browser compatibility issues
- Can be fixed in separate PR

## Best Practices

✅ **Always passing**: Unit + Integration + Logging tests  
✅ **Required for merge**: Main CI must pass  
✅ **Optional**: E2E tests (nice to have)  
✅ **Run locally first**: Use `./ci_check.sh`  

## Quick Commands

```bash
# Run all CI tests locally (excluding E2E)
pytest tests/test_operations.py tests/test_main.py tests/test_logging.py -v

# Run with coverage
pytest tests/test_operations.py tests/test_main.py tests/test_logging.py --cov=. --cov-report=html

# Run E2E tests
pytest tests/test_e2e.py -v

# Full local CI check
./ci_check.sh
```
