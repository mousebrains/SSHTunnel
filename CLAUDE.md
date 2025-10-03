# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

SSHTunnel creates and maintains reverse SSH tunnels for remote access across firewalls. The primary use case is maritime/shipboard computing where a ship-side computer behind a firewall needs to be accessible from shore.

**Core Components:**
- `tunnel.py` - SSH tunnel client that creates and maintains reverse tunnel connections
- `install.py` - Systemd service installer that generates and installs tunnel as a system service
- `SSHtunnel.template` - Systemd service template file with placeholder variables
- `hostnames.yaml` - Maps local hostnames to remote port numbers

## Architecture

### tunnel.py - Tunnel Client
- Uses `TPWUtils.Logger` for logging configuration (adds `--verbose`, `--debug`, `--logfile` arguments)
- Builds SSH command with reverse tunnel: `ssh -N -x -T -R remotePort:localHost:localPort host`
- Implements retry logic with configurable `--attempts` and `--delay`
- Checks subprocess return codes and logs stdout/stderr on failures
- Exits with code 1 on failure (for systemd restart detection)

**Key SSH options:**
- `-N`: No remote command execution
- `-x`: Disable X11 forwarding
- `-T`: Disable pseudo-terminal allocation
- `-R`: Reverse tunnel specification
- `ExitOnForwardFailure=yes`: Exit if tunnel cannot be established
- `ServerAliveInterval` and `ServerAliveCountMax`: Keep connection alive

### install.py - Service Installer
- Reads `SSHtunnel.template` and performs variable substitution using regex
- Uses `hostnames.yaml` to auto-determine port numbers based on `socket.gethostname()`
- Handles username detection with fallback: tries `os.getlogin()`, falls back to `pwd.getpwuid(os.getuid())`
- Uses `shutil.which()` to find system executables (systemctl, cp, chmod, sudo) with hardcoded fallbacks
- Compares existing service file to avoid unnecessary updates (using `barebones()` function)
- Writes to temp file then copies with sudo to `/etc/systemd/system/`
- Automatically enables and starts the service

**Template placeholders:**
- `@DATE@`, `@GENERATED@`, `@USERNAME@`, `@GROUPNAME@`, `@DIRECTORY@`, `@EXECUTABLE@`, `@LOGFILE@`, `@HOSTNAME@`, `@PORT@`, `@RESTARTSECONDS@`

## Development Commands

### Setup
```bash
pip install -r requirements.txt  # Install dependencies (PyYAML, TPWUtils)
pip install -e .[dev]            # Install dev dependencies (pytest, mypy, ruff)
```

### Testing
```bash
pytest tests/ -v                 # Run all tests with verbose output
pytest tests/test_tunnel.py -v   # Run specific test file
pytest tests/ --cov              # Run with coverage report
```

### Linting & Type Checking
```bash
ruff check .                     # Run linter (excludes TPWUtils by default in practice)
ruff check . --fix              # Auto-fix issues
mypy --ignore-missing-imports tunnel.py install.py  # Type check main files
```

### Manual Testing
```bash
# Test tunnel client directly (requires remote host setup)
./tunnel.py --host shore.example.com --remotePort 12345 --username myuser --attempts 3

# Test service installation (requires sudo)
sudo ./install.py --hostname shore.example.com --port 12345

# Check service status
sudo systemctl status SSHtunnel.service
sudo journalctl -u SSHtunnel.service -n 50
```

## Important Implementation Details

### Argument Naming Convention
- Use `--attempts` (not `--retries`) - represents total number of connection attempts, not retries after first attempt
- `--remotePort` is required in tunnel.py to ensure tunnel is created

### Error Handling
- Use `except Exception:` not bare `except:` to avoid catching SystemExit/KeyboardInterrupt
- All subprocess.run() calls should have `check=True` for proper error detection
- Subprocess failures should log return code, stdout, and stderr

### Compatibility
- Python 3.10+ required
- Uses `Optional[str]` type hints (not `str | None`) for backward compatibility
- Executable paths use `shutil.which()` for cross-platform compatibility (BSD, NixOS, etc.)
- `os.makedirs()` calls use `exist_ok=True` to prevent race conditions

### String Formatting
- Use f-strings consistently (not %-formatting)
- Example: `logging.info(f"Starting attempt {attempt + 1} of {args.attempts}")`

### Dependencies
- `TPWUtils` is installed via pip from GitHub (was previously a git submodule)
- If adding new dependencies, update both `requirements.txt` and `pyproject.toml`

## Configuration Files

### hostnames.yaml Format
```yaml
# Hostname to port mapping (proper YAML, not JSON)
ship-hostname-1: 11000
ship-hostname-2: 11001
```

### Service Template Variables
When modifying `SSHtunnel.template`, variables must match regex patterns in `install.py` (lines 110-119):
- Pattern: `@VARIABLENAME@`
- Substituted using `re.sub(r"@VARIABLENAME@", value, input)`
