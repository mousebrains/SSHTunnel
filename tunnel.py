#! /usr/bin/env python3
#
# Build a ssh connection to a target and add a tunnel back to my local ssh port
#
# Jan-2022, Pat Welch, pat@mousebrains.com

"""SSH tunnel client that maintains a reverse tunnel connection to a remote host."""

import logging
import subprocess
import sys
import time
from argparse import ArgumentParser, Namespace

from TPWUtils import Logger

parser: ArgumentParser = ArgumentParser()
Logger.addArgs(parser)
grp = parser.add_argument_group(description="SSH related options")
grp.add_argument("--ssh", type=str, default="/usr/bin/ssh", help="SSH binary to use")
grp.add_argument("--interval", type=int, default=60, help="Value to set ServerAliveInterval to")
grp.add_argument("--count", type=int, default=3, help="Value to set ServerAliveCountMax to")
grp.add_argument("--identity", type=str, help="Public key filename")
grp.add_argument("--username", type=str, help="Remote username")
grp.add_argument("--host", type=str, required=True, help="Remote hostname")
grp.add_argument("--port", type=int, help="Remote host port to connect to")
grp.add_argument("--remotePort", type=int, required=True, help="Remote Port Number")
grp.add_argument("--localPort", type=int, default=22, help="Local Port Number")
grp.add_argument("--localHost", type=str, default="localhost", help="Local host to forward to")
grp.add_argument("--attempts", type=int, default=1, help="Number of connection attempts")
grp.add_argument("--delay", type=float, default=60, help="Number of seconds between attempts")
args: Namespace = parser.parse_args()

Logger.mkLogger(args)

cmd: list[str] = [args.ssh,
       "-N",  # Do not execute remote command
       "-x",  # Disable X11 forwarding
       "-T",  # Disable pseudo-terminal allocation
       "-o", "ExitOnForwardFailure=yes", # If tunnel can't be set up exit
       ]

if args.identity:
    cmd.extend(("-i", args.identity))

if args.interval > 0:
    cmd.extend(("-o", f"ServerAliveInterval={args.interval}"))
    if args.count > 0:
        cmd.extend(("-o", f"ServerAliveCountMax={args.count}"))

cmd.extend(("-R", f"{args.remotePort}:{args.localHost}:{args.localPort}"))

if args.username:
    cmd.extend(("-l", args.username))

if args.port:
    cmd.extend(("-p", args.port))

cmd.append(args.host)

logging.info(f"Command: {' '.join(cmd)}")

for attempt in range(args.attempts):
    logging.info(f"Starting attempt {attempt + 1} of {args.attempts}")
    try:
        s: subprocess.CompletedProcess[bytes] = subprocess.run(
                cmd,
                capture_output=True,
                shell=False,
                check=False,  # Don't raise exception, we handle it manually
                )
        if s.returncode != 0:
            logging.error(f"SSH tunnel failed with return code {s.returncode}")
            logging.error(f"stdout: {s.stdout.decode('utf-8', errors='ignore')}")
            logging.error(f"stderr: {s.stderr.decode('utf-8', errors='ignore')}")
        else:
            logging.info("SSH connection terminated normally")
    except Exception:
        logging.exception(f"Error in {cmd}")

    if (args.delay > 0) and ((attempt + 1) < args.attempts):
        logging.info(f"Sleeping {args.delay} seconds before the next connection attempt")
        time.sleep(args.delay)

logging.error(f"Exceeded maximum number of attempts, {args.attempts}")
sys.exit(1)
