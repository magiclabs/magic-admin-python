# Magic Admin Python SDK

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![PyPI version](https://badge.fury.io/py/magic-admin.svg)](https://badge.fury.io/py/magic-admin)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](https://opensource.org/license/mit)

The Magic Admin Python SDK provides a simple and powerful way to integrate Magic's authentication system into your Python applications. Handle [DID Tokens](https://docs.magic.link/embedded-wallets/authentication/features/decentralized-id#decentralized-id-did-tokens) and interact with Magic API endpoints with ease.

## 📚 Documentation

📖 **Full Documentation**: [Magic Python SDK Docs](https://docs.magic.link/embedded-wallets/sdk/server-side/python)

## 🚀 Quick Start

### Installation

```bash
# Using pip
pip install magic-admin

# Using uv
uv add magic-admin
```

### Basic Usage

```python
from magic_admin import Magic

# Initialize with your API secret key
magic = Magic(api_secret_key='your_api_secret_key_here')

# Validate a DID token
try:
    magic.Token.validate('DID_TOKEN_FROM_CLIENT')
    print("Token is valid!")
except Exception as e:
    print(f"Token validation failed: {e}")
```

### Environment Variable Configuration

You can also load your API secret key from an environment variable:

```bash
export MAGIC_API_SECRET_KEY="your_api_secret_key_here"
```

```python
from magic_admin import Magic

# Automatically uses MAGIC_API_SECRET_KEY environment variable
magic = Magic()
```

> **Note**: The API secret key passed directly to `Magic()` takes precedence over the environment variable.

### Network Configuration

Customize network behavior for your application:

```python
magic = Magic(
    api_secret_key='your_key',
    retries=5,           # Number of retry attempts
    timeout=10,          # Request timeout in seconds
    backoff_factor=0.03  # Exponential backoff factor
)
```

## 🔧 Development

### Prerequisites

- Python 3.11+
- Git

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/magiclabs/magic-admin-python.git
cd magic-admin-python

# Create virtual environment and install dependencies
make development

# Activate the virtual environment
source virtualenv_run/bin/activate
```

### Running Tests

```bash
# Run tests against all supported Python versions (3.11, 3.12, 3.13)
make test

# Run tests with coverage
make test
```

### Code Quality

This project uses [pre-commit](https://pre-commit.com/) to maintain code quality. Hooks run automatically on every commit.

```bash
# Run pre-commit hooks manually
pre-commit run --all-files

# Install pre-commit hooks
pre-commit install
```

### Cleanup

```bash
# Remove virtual environment, tox logs, and pytest cache
make clean
```

## 📋 Requirements

- **Python**: 3.11+
- **Dependencies**: See [requirements.txt](requirements.txt)
- **Development**: See [requirements-dev.txt](requirements-dev.txt)

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Workflow

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests: `make test`
5. Run pre-commit: `pre-commit run --all-files`
6. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](https://opensource.org/license/mit) file for details.

## 📝 Changelog

See [CHANGELOG.md](CHANGELOG.md) for a detailed history of changes.

## 🔗 Links

- [Magic Documentation](https://docs.magic.link)
- [Magic Dashboard](https://dashboard.magic.link)
- [Magic Python SDK Docs](https://docs.magic.link/embedded-wallets/sdk/server-side/python)
- [DID Token Documentation](https://docs.magic.link/embedded-wallets/authentication/features/decentralized-id#decentralized-id-did-tokens)
