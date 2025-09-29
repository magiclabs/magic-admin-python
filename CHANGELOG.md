## `2.1.2` - 2025-09-29

#### 🚀 New Features

- **Added Utility Methods for 100% JavaScript SDK Parity**
  - `utils.parse_authorization_header(header)` - Extract DID tokens from HTTP Authorization headers
  - `utils.validate_token_ownership(did_token, contract_address, contract_type, rpc_url, token_id?)` - NFT ownership validation for Token Gating
  - Both methods match the exact functionality available in the JavaScript SDK

---

## `2.0.1` - 2025-07-25

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

## `1.0.0` - 2023-07-10

#### Added

- PR-#87: Add Magic Connect Admin SDK support for Token Resource [#111](https://github.com/magiclabs/magic-admin-js/pull/111) ([@magic-ravi](https://github.com/magic-ravi))
  - [Security Enhancement]: Validate `aud` using Magic client ID.
  - Pull client ID from Magic servers if not provided in constructor.

## `0.3.3` - 2023-05-02

#### Changed

- PR-#77: Removing NFT functionality, clients will interact with the NFT API directly via API calls.

## `0.3.2` - 2023-03-24

#### Added

- PR-#69: Patch bad formatting of request

## `0.3.1` - 2023-03-24

#### Added

- PR-#67: Patch module not found fixed for new NFT module.

## `0.3.0` - 2023-03-23

#### Added

- PR-#66: Create paths for minting an NFT through Magic delivery service.

## `0.2.0` - 2023-03-16

#### Added

- PR-#50: Split up DIDTokenError into DIDTokenExpired, DIDTokenMalformed, and DIDTokenInvalid.

## `0.1.0` - 2023-03-16

#### Added

- PR-#46: Support multi-chain wallets in get_metadata calls

## `0.0.5` - 2021-06-23

#### Fixed

- <PR-#34> Relax dependency version requirement constraints

## `0.0.4` - 2020-04-24

#### Changed

- PR-#14: Update external document link.

## `0.0.3` - 2020-04-18

#### Added

- Initial release for 0.0.3. (No details available.)

## `0.0.2` - 2020-04-12

#### Added

- Initial release for 0.0.2. (No details available.)

## `0.0.1` - 2020-04-12

#### Added

- Initial release for 0.0.1. (No details available.)

## `0.0.0.0` - 2020-04-12

#### Added

- Initial release for 0.0.0.0. (No details available.)
