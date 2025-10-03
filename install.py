#! /usr/bin/env python3
#
# Install a service for the SSH tunnel from this machine to shore
# so somebody on shore can log into the shipboard machine.
#
# Feb-2022, Pat Welch, pat@mousebrains.com

"""Install systemd service for SSH reverse tunnel."""

import os
import pwd
import re
import shutil
import socket
import subprocess
import sys
import time
from argparse import ArgumentParser, Namespace
from tempfile import NamedTemporaryFile
from typing import Any

import yaml


def find_executable(name: str, fallback: str) -> str:
    """Find executable in PATH, falling back to common location."""
    found: str | None = shutil.which(name)
    return found if found else fallback

def barebones(content: str) -> list[str]:
    """Remove comments and blank lines from content."""
    lines: list[str] = []
    for line in content.split("\n"):
        line = line.strip()
        if (len(line) == 0) or (line[0] == "#"):
            continue
        lines.append(line)
    return lines

parser: ArgumentParser = ArgumentParser()
parser.add_argument("--template", type=str, default="SSHtunnel.template",
        help="Service template file to generate local service file from")
parser.add_argument("--service", type=str, default="SSHtunnel", help="Service name")
parser.add_argument("--serviceDirectory", type=str, default="/etc/systemd/system",
        help="Where to copy service file to")
grp = parser.add_argument_group(description="Service file translation related options")
grp.add_argument("--hostname", type=str, default="arcterx", help="Remote hostname")
grp.add_argument("--port", type=int, help="Port number on remote host")
grp.add_argument("--username", type=str, help="Local user to run service as")
grp.add_argument("--group", type=str, help="Local group to run service as")
grp.add_argument("--logfile", type=str,
        default=os.path.join(os.path.abspath(os.path.expanduser("~/logs")), "SSHtunnel.log"),
        help="Local logfile directory")
grp.add_argument("--directory", type=str, help="Directory to change to for running the service")
grp.add_argument("--restartSeconds", type=int, default=300,
        help="Time before restarting the service after the previous instance exits")
grp.add_argument("--executable", type=str, default="tunnel.py",
        help="Executable name to be executed by service")
parser.add_argument("--force", action="store_true", help="Force writing a new file")
parser.add_argument("--systemctl", type=str,
        default=find_executable("systemctl", "/usr/bin/systemctl"),
        help="systemctl executable")
parser.add_argument("--cp", type=str,
        default=find_executable("cp", "/bin/cp"),
        help="cp executable")
parser.add_argument("--chmod", type=str,
        default=find_executable("chmod", "/bin/chmod"),
        help="chmod executable")
parser.add_argument("--sudo", type=str,
        default=find_executable("sudo", "/usr/bin/sudo"),
        help="sudo executable")
parser.add_argument("--knownHosts", type=str, help="Known host to port dictionary YAML file")
args: Namespace = parser.parse_args()

root: str = os.path.dirname(os.path.abspath(__file__))

if args.knownHosts is None:
    args.knownHosts = os.path.join(root, "hostnames.yaml")

with open(args.knownHosts) as fp:
    known_hosts: dict[str, Any] = yaml.safe_load(fp)

hostname: str = socket.gethostname()

if args.port is None:
    if hostname not in known_hosts:
        parser.error(f"Unknown host, '{hostname}', so you must specify --port")
    args.port = known_hosts[hostname]

if args.service is None:
    args.service = f"SSHtunnel.service.{hostname}"

if args.username is None: # Get this process's username
    try:
        # Try getlogin first for sudo compatibility
        args.username = os.getlogin()
    except OSError:
        # Fallback to pwd module for non-interactive environments (cron, systemd, containers)
        args.username = pwd.getpwuid(os.getuid()).pw_name

if args.group is None: # Get this process's group
    args.group = args.username

if args.directory is None: # working directory to move to
    args.directory = "~/logs"

with open(os.path.join(root, args.template)) as fp:
    input: str = fp.read() # Load the entire template

wd: str = os.path.abspath(os.path.expanduser(args.directory)) # Working directory

input = re.sub(r"@DATE@", "Generated on " + time.asctime(), input)
input = re.sub(r"@GENERATED@", str(args), input)
input = re.sub(r"@USERNAME@", args.username, input)
input = re.sub(r"@GROUPNAME@", args.group, input)
input = re.sub(r"@DIRECTORY@", wd, input)
input = re.sub(r"@EXECUTABLE@", os.path.join(root, args.executable), input)
input = re.sub(r"@LOGFILE@", args.logfile, input)
input = re.sub(r"@HOSTNAME@", args.hostname, input)
input = re.sub(r"@PORT@", str(args.port), input)
input = re.sub(r"@RESTARTSECONDS@", str(args.restartSeconds), input)

fn: str = os.path.join(args.serviceDirectory, f"{args.service}.service")

if not args.force and os.path.exists(fn):
    try:
        with open (fn) as fp:
            current: list[str] = barebones(fp.read()) # Current contents
            proposed: list[str] = barebones(input) # What we want to write
            if current == proposed:
                print("No need to update, identical")
                sys.exit(0)
    except Exception:
        pass

if not os.path.isdir(wd):
    print("Making", wd)
    os.makedirs(wd, mode=0o755, exist_ok=True)

# Write to a temporary file, then copy as root via sudo
with NamedTemporaryFile(mode="w", delete=False) as fp:  # type: ignore[assignment]
    fp.write(input)
    fp.flush()
    temp_name = fp.name

print("Writing to", fn)
subprocess.run((args.sudo, args.cp, temp_name, fn), shell=False, check=True)
subprocess.run((args.sudo, args.chmod, "0644", fn), shell=False, check=True)
os.unlink(temp_name)

print("Forcing reload of daemon")
subprocess.run((args.sudo, args.systemctl, "daemon-reload"), shell=False, check=True)

print(f"Enabling {args.service}")
subprocess.run((args.sudo, args.systemctl, "enable", args.service), shell=False, check=True)

print(f"Starting {args.service}")
subprocess.run((args.sudo, args.systemctl, "restart", args.service), shell=False, check=True)

print(f"Status {args.service}")
s: subprocess.CompletedProcess[bytes] = subprocess.run(
        (args.sudo, args.systemctl, "--no-pager", "status", args.service),
        shell=False, check=True)
