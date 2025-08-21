# Publishing to PyPI

## Prerequisites

1. Install twine for uploading to PyPI:
```bash
pip install twine
```

2. Create PyPI account at https://pypi.org/account/register/
3. Create API token at https://pypi.org/manage/account/token/

## Build the Package

```bash
# Clean previous builds
rm -rf dist/ build/ *.egg-info/

# Build the package
python -m build
```

## Test Upload (TestPyPI)

```bash
# Upload to TestPyPI first
twine upload --repository testpypi dist/*

# Install from TestPyPI to test
pip install --index-url https://test.pypi.org/simple/ ANAL
```

## Production Upload

```bash
# Upload to PyPI
twine upload dist/*
```

## Environment Variables

Set these in your environment or CI/CD:

```bash
export TWINE_USERNAME=__token__
export TWINE_PASSWORD=your_api_token_here
```

## Automated Release (GitHub Actions)

Create `.github/workflows/release.yml`:

```yaml
name: Release to PyPI

on:
  push:
    tags:
      - 'v*'

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.12'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install build twine
    
    - name: Build package
      run: python -m build
    
    - name: Upload to PyPI
      env:
        TWINE_USERNAME: __token__
        TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
      run: twine upload dist/*
```

## Version Management

Update version in `pyproject.toml` before each release:

```toml
[project]
version = "0.1.1"  # Increment this
```

## Install After Publishing

```bash
pip install ANAL
```

## Verify Installation

```bash
anal-admin version
anal-admin startproject test_project
```
