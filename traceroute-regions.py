# this script tries to reach targets in the same geographic area

from scapy.all import *
import logging
import argparse
import csv
from datetime import datetime
import json
from pathlib import Path
import urllib.request
from pathlib import Path
from ipaddress import IPv4Network
from common import *
import subprocess as s

parser = argparse.ArgumentParser(
    prog="reach-single-target",
    description="reach the same target overtime and saves the hops related to starlink",
)
parser.add_argument(
    "--verbose", "-v", help="verbose", action=argparse.BooleanOptionalAction
)
parser.add_argument(
    "--starlink", "-s", help="use starlink?", action=argparse.BooleanOptionalAction
)

parser.add_argument("--asndb", help="asndb file location")
parser.add_argument("--region_file", "-r", help="region file")
parser.add_argument("--directory", "-d", help="where to store files", required=True)
args = parser.parse_args()

if args.verbose:
    logging.getLogger().setLevel(logging.DEBUG)
    logging.getLogger("urllib3").setLevel(logging.WARNING)

else:
    logging.getLogger().setLevel(logging.INFO)

with open(args.region_file, "r") as f:
    data = json.load(f)

for t in data["prefixes"]:
    ip = t["ip"]
    scope = t["scope"]
    dir = f"{args.directory}"
    Path(dir).mkdir(parents=True, exist_ok=True)
    logging.debug(f"tracerouting {scope} {ip}")


    if args.starlink:
        with open(f"{dir}/{scope}-{ip}-icmp-starlink-4.csv", "a+") as f:
            cmd=["mtr","--csv","-4",'-I',"enp1s0f2",ip]
            s.call(cmd, stdout=f)

        with open(f"{dir}/{scope}-{ip}-udp-starlink-4.csv", "a+") as f:
            cmd=["mtr","--csv","-4","-u",'-I',"enp1s0f2",ip]
            s.call(cmd, stdout=f)
        
        with open(f"{dir}/{scope}-{ip}-tcp-starlink-4.csv", "a+") as f:
            cmd=["traceroute","--csv","-4","-T",'-I',"enp1s0f2",ip]
            s.call(cmd, stdout=f)
    else:
        with open(f"{dir}/{scope}-{ip}-icmp-4.csv", "a+") as f:
            cmd=["mtr","--csv","-4",ip]
            s.call(cmd, stdout=f)

        with open(f"{dir}/{scope}-{ip}-udp-4.csv", "a+") as f:
            cmd=["mtr","--csv","-4","-u",ip]
            s.call(cmd, stdout=f)
        
        with open(f"{dir}/{scope}-{ip}-tcp-4.csv", "a+") as f:
            cmd=["mtr","--csv","-4","-T",ip]
            s.call(cmd, stdout=f)
