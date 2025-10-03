# SSH Tunnel

Establish a reverse SSH tunnel so a computer on one side of a firewall can be accessed from the other side.

## Overview

This tool creates a reverse SSH tunnel from a "ship side" computer (behind a firewall) to a "shore side" computer (publicly accessible), allowing connections to be originated from shore to ship.

## Installation

### 1. Clone the repository

```bash
git clone git@github.com:mousebrains/SSHTunnel.git
cd SSHTunnel
```

### 2. Install Python dependencies

```bash
pip install -r requirements.txt
```

This will install:
- PyYAML - for configuration file parsing
- TPWUtils - utility library from GitHub

## Configuration

### Shore Side (Remote Host)

Configure the SSH daemon to keep connections alive by setting `ClientAliveInterval` and `ClientAliveCountMax`.

On Ubuntu systems:
```bash
sudo cp 01.ClientAlive.conf /etc/ssh/sshd_config.d/
sudo systemctl restart sshd
```

### Ship Side (Local Host)

1. **Configure hostnames**: Edit `hostnames.yaml` to map your local hostname to a remote port number:
   ```yaml
   my-ship-host: 12345
   ```

2. **Set up SSH keys**: Ensure you have SSH key-based authentication configured for the remote host.

## Usage

### Manual Tunnel

Create an SSH tunnel manually:

```bash
./tunnel.py --host shore.example.com --remotePort 12345 --username myuser
```

Options:
- `--host`: Remote hostname to connect to (required)
- `--remotePort`: Port on remote host for reverse tunnel
- `--localPort`: Local SSH port (default: 22)
- `--username`: Remote username for SSH connection
- `--identity`: Path to SSH private key
- `--attempts`: Number of connection attempts (default: 1)
- `--delay`: Seconds between attempts (default: 60)

### Install as systemd Service

Install the tunnel as a systemd service for automatic startup:

```bash
sudo ./install.py --hostname shore.example.com --port 12345
```

Options:
- `--hostname`: Remote hostname (default: arcterx)
- `--port`: Remote port number (will use hostnames.yaml if not specified)
- `--username`: Local user to run service as (default: current user)
- `--service`: Service name (default: SSHtunnel)
- `--logfile`: Path to log file

The service will:
- Start automatically on boot
- Restart automatically after failures
- Log to the specified log file

Check service status:
```bash
sudo systemctl status SSHtunnel.service
```

## Troubleshooting

### Connection fails immediately
- Verify SSH key authentication works: `ssh -i ~/.ssh/id_rsa user@shore.example.com`
- Check firewall rules on both sides
- Verify the remote host allows reverse tunneling (`GatewayPorts` in sshd_config)

### TPWUtils not found
If you get `ImportError: No module named 'TPWUtils'`:
```bash
pip install git+https://github.com/mousebrains/TPWUtils.git
```

### Service won't start
Check logs:
```bash
sudo journalctl -u SSHtunnel.service -n 50
```

### Connection drops frequently
- Increase `ServerAliveInterval` and `ServerAliveCountMax` on shore side
- Check network stability
- Review logs for error messages

## License

GPL-3.0
