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
import subprocess
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

if args.starlink:
    conf.route.add(net="0.0.0.0/0", gw="192.168.1.1")

with open(args.region_file, "r") as f:
    data = json.load(f)

for t in data["prefixes"]:
    ip = t["ip"]
    scope = t["scope"]
    dir = f"{args.directory}"
    Path(dir).mkdir(parents=True, exist_ok=True)
    # with open()
    # logging.debug({dir})
    # qua con sto indirizzo ci facciamo: traceroute con udp icmp tcp

    reach_target(target=ip, asndb=args.asndb, filename=f"{dir}/{scope}-{ip}")



# f = open("blah.txt", "w")
# subprocess.call(["/home/myuser/run.sh", "/tmp/ad_xml",  "/tmp/video_xml"], stdout=f)