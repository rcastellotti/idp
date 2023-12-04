"""
traceroute an host, using different methods, using both starlink
and the default cabled connection
"""
import argparse
import logging
import os
import csv
from pathlib import Path
from datetime import datetime
from scapy.config import conf
from common import traceroute


parser = argparse.ArgumentParser(prog="traceroute")
parser.add_argument(
    "--verbose", "-v", help="verbose", action=argparse.BooleanOptionalAction
)
parser.add_argument(
    "--starlink", "-s", help="use starlink?", action=argparse.BooleanOptionalAction
)
parser.add_argument("--directory", "-d", help="where to store files", required=True)
parser.add_argument("--asndb", "-a", help="asndb file location", required=True)
parser.add_argument("--region_file", "-r", help="region file  (csv)", required=True)
args = parser.parse_args()

if args.verbose:
    logging.getLogger().setLevel(logging.DEBUG)
    logging.getLogger("urllib3").setLevel(logging.WARNING)

else:
    logging.getLogger().setLevel(logging.INFO)


def run_traceroute(filename):
    """
    run the traceroute
    """
    logging.debug("tracerouting %s", filename)
    file_exists = os.path.isfile(filename)

    with open(filename, "a", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(("timestamp", "ttl", "ip", "hostname", "asn"))
        res = traceroute(ip, p, asndb=args.asndb)
        writer.writerows(res)


# sudo ./perform_cloud_traceroutes.py \
#                                          -d gino \
#                                          -a ../idp-castellotti-data/ipasn_20230315.dat
# -r ../idp-castellotti-data/targets.csv

with open(args.region_file, "r", encoding="utf-8") as csvfile:
    next(csvfile)  # skipping the header
    reader = csv.reader(csvfile)

    for row in reader:
        provider, region, ip = row
        d = args.directory
        Path(d + "/" + provider).mkdir(parents=True, exist_ok=True)

        for p in ["ICMP", "UDP", "TCP"]:
            dt = datetime.now().isoformat()
            results = []

            run_traceroute(f"{d}/{provider}/{region}-{ip}-{dt}-{p}-normal.csv")

            conf.route.add(net="0.0.0.0/0", gw="192.168.200.11")
            run_traceroute(f"{d}/{provider}/{region}-{ip}-{dt}-{p}-starlink.csv")
            conf.route.delt(net="0.0.0.0/0", gw="192.168.200.11")
