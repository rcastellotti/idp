"""
Reach the same target overtime and saves the hops related to AS14593
"""

import logging
import os
import csv
import argparse
from datetime import datetime
from pathlib import Path
import pyasn
from scapy.config import conf
from scapy.layers.inet import IP, ICMP
from scapy.sendrecv import sr1

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
parser.add_argument("--directory", "-d", help="where to store files", required=True)


def main():
    for t in targets:
        logging.debug("reaching %s", t)
        time = datetime.now()
        Path(args.directory).mkdir(parents=True, exist_ok=True)
        filename = f"{args.directory}/{t}.csv"
        file_exists = os.path.isfile(filename)
        with open(filename, "a", encoding="utf-8") as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(["time", "hop#", "ip"])
            # we see the first hop in AS14593 in 4th position at earliest
            for i in range(4, 6):
                myPacket = IP(dst=t, ttl=i) / ICMP()
                res = sr1(myPacket, verbose=0, timeout=3)
                if res:
                    logging.debug(res.src)
                    src = res.src
                    lookup = asndb.lookup(src)
                    if lookup[0] == 14593:
                        writer.writerow([time, i, src])


if __name__ == "__main__":
    args = parser.parse_args()
    if args.verbose:
        logging.getLogger().setLevel(logging.INFO)
    main()
