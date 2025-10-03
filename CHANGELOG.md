# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-01-03

### Added
- Comprehensive README with installation, configuration, usage, and troubleshooting sections
- Test suite with 13 unit tests covering core functionality
- GitHub Actions CI/CD workflow for automated testing
- Type hints throughout codebase for better IDE support and error detection
- Module and function docstrings for improved documentation
- `pyproject.toml` for modern Python package management
- `CONTRIBUTING.md` with development guidelines
- `requirements.txt` with project dependencies
- Warning when `--remotePort` not specified in tunnel.py
- Fallback for `os.getlogin()` to support non-interactive environments

### Changed
- Renamed `--retries` argument to `--attempts` for clarity
- Changed from `%-formatting` to f-strings throughout codebase
- Converted `hostnames.yaml` from JSON syntax to proper YAML format
- Exit with code 1 instead of 0 when tunnel fails after all attempts
- Improved error logging with detailed stdout/stderr output
- Changed logging level from `info` to `error` when exceeding attempts

### Changed
- Converted TPWUtils from git submodule to pip dependency

### Fixed
- Fixed bare `except:` clause to `except Exception:` in install.py
- Added `exist_ok=True` to `os.makedirs()` to prevent race condition
- Added `check=True` to chmod subprocess call for proper error handling
- Added return code checking for SSH subprocess execution
- Fixed README typo: `010.ClientAlive.conf` → `01.ClientAlive.conf`
- Updated service template to use `--attempts` instead of `--retries`

### Security
- Added proper exception handling to avoid catching system signals
- Added subprocess error checking to detect failures

## [Unreleased]

### Planned
- Support for multiple simultaneous tunnels
- Configuration file support
- Automatic retry backoff strategy
- Health check endpoint

[1.0.0]: https://github.com/mousebrains/SSHTunnel/releases/tag/v1.0.0
