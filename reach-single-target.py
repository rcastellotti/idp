# this script tries to reach the same target overtime and saves the hops related to starlink
from scapy.all import *
import pyasn
import logging
import argparse
import csv
from datetime import datetime
import os
from pathlib import Path

asndb = pyasn.pyasn("/root/idp-castellotti-data/ipasn_20230315.dat")
# use starlink
conf.route.add(net="0.0.0.0/0", gw="192.168.1.1")

targets = (
    "caida.org",
    "utu.fi",
    "garr.it",
    "tum.de",
    "mit.edu",
    "unibuc.ro",
    "ox.ac.uk",
    "cam.ac.uk",
    "www.uct.ac.za",
)

parser = argparse.ArgumentParser(
    prog="reach-single-target",
    description="reach the same target overtime and saves the hops related to starlink",
)
parser.add_argument(
    "--verbose", "-v", help="verbose", action=argparse.BooleanOptionalAction
)
parser.add_argument(
    "--directory", "-d", help="where to store files", required=True
)
args = parser.parse_args()
if args.verbose:
    logging.getLogger().setLevel(logging.DEBUG)
    logging.getLogger("urllib3").setLevel(logging.WARNING)

else:
    logging.getLogger().setLevel(logging.INFO)

for t in targets:
    logging.debug(f"reaching {t}")
    time = datetime.now()
    Path(args.directory).mkdir(parents=True, exist_ok=True)
    filename=f"{args.directory}/{t}.csv"
    file_exists=os.path.isfile(filename)
    f=open(filename, "a")
    writer = csv.writer(f)
    if not file_exists:
        writer.writerow(["time", "hop#", "ip"])

    for i in range(4,6):
        myPacket = IP(dst="www.caida.org", ttl=i) / ICMP()
        res = sr1(myPacket, verbose=0, timeout=3)
        if res:
            logging.debug(res.src)
            src = res.src
            lookup = asndb.lookup(src)
            if lookup[0] == 14593:
                writer.writerow([time, i, src])
