## `2.0.0` - 2025-07-25

#### 🚀 Major Changes

- **Python Version Support**: Updated minimum Python version to 3.11+
  - Dropped support for Python 3.10 and below
  - Development environment uses Python 3.13

#### 📦 Dependencies

- Updated core dependencies: `web3` (6→7.12.1), `websockets` (10.0→15.0.1), `requests` (2.32.4)
- Updated development dependencies: `pre-commit` (3.7.0→4.2.0), `pytest` (8.4.1), `coverage` (7.9.2)

#### 🔧 Improvements

- Fixed pre-commit hook compatibility issues
- Improved test coverage and multi-version testing
- Enhanced documentation and development workflow
- Updated all configuration files for Python 3.11+ support

---

## `1.0.0` - 07/05/2023

#### Added

- PR-#87: Add Magic Connect Admin SDK support for Token Resource [#111](https://github.com/magiclabs/magic-admin-js/pull/111) ([@magic-ravi](https://github.com/magic-ravi))
  - [Security Enhancement]: Validate `aud` using Magic client ID.
  - Pull client ID from Magic servers if not provided in constructor.

## `0.3.3` - 05/02/2023

#### Changed

- PR-#77: Removing NFT functionality, clients will interact with the NFT API directly via API calls.

## `0.3.2` - 03/21/2023

#### Added

- PR-#69: Patch bad formatting of request

## `0.3.1` - 03/21/2023

#### Added

- PR-#67: Patch module not found fixed for new nft module

## `0.3.0` - 03/20/2023

#### Added

- PR-#66: Create paths for minting an NFT through magic delivery service.

## `0.2.0` - 1/04/2023

#### Added

- PR-#50: Split up DIDTokenError into DIDTokenExpired, DIDTokenMalformed, and DIDTokenInvalid.

## `0.1.0` - 11/30/2022

#### Added

- PR-#46: Support mult-chain wallets in get_metadata calls

## `0.0.5` - 06/23/2021

#### Fixed

- <PR-#34> Relax dependency version requirement constraints

## `0.0.4` - 04/23/2020

#### Changed

- PR-#14: Update external document link.
