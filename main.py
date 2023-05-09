from scapy.all import *
from scapy.layers.inet import UDP
import time
import json
import argparse
from common import traceroute
import csv
from pathlib import Path

parser = argparse.ArgumentParser(prog="traceroute")

parser.add_argument(
    "--verbose", "-v", help="verbose", action=argparse.BooleanOptionalAction
)
parser.add_argument(
    "--starlink", "-s", help="use starlink?", action=argparse.BooleanOptionalAction
)
parser.add_argument("--directory", "-d", help="where to store files", required=True)
parser.add_argument("--asndb", help="asndb file location", required=True)
parser.add_argument("--region_file", "-r", help="region file  (csv)",required=True)

args = parser.parse_args()

if args.verbose:
    logging.getLogger().setLevel(logging.DEBUG)
    logging.getLogger("urllib3").setLevel(logging.WARNING)

else:
    logging.getLogger().setLevel(logging.INFO)

with open(args.region_file, "r") as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        print(row)

# for ip in data["prefixes"]:
#     ip = t["ip"]
#     scope = t["scope"]
#     dir = f"{args.directory}"
#     Path(dir).mkdir(parents=True, exist_ok=True)
#     logging.debug(f"tracerouting {scope} {ip}")
#     for p in ["ICMP", "UDP", "TCP"]:
#         filename = f"{dir}/{scope}-{ip}-{p}-4.csv"
#         if args.starlink:
#             logging.debug("using starlink")
#             conf.route.add(net="0.0.0.0/0", gw="192.168.1.1")
#             filename = f"{dir}/{scope}-{ip}-{p}-starlink-4.csv"

#         file_exists = os.path.isfile(filename)
#         f = open(filename, "a")
#         writer = csv.writer(f)
#         if not file_exists:
#             writer.writerow(("timestamp", "ttl", "ip", "hostname", "asn"))
#         results = traceroute(ip, p, asndb=args.asndb)
#         writer.writerows(results)
