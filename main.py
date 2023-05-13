from scapy.all import *
from scapy.layers.inet import UDP
import time
import argparse
from common import traceroute
import csv
from pathlib import Path
from datetime import datetime

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

def run_traceroute(filename,type):
    logging.debug(f"traceroute {filename}")
    file_exists = os.path.isfile(filename)

    with open(filename, "a") as f:

        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(("timestamp", "ttl", "ip", "hostname", "asn"))
        results = traceroute(ip, p, asndb=args.asndb)
        writer.writerows(results)

    # with open(f"{dir}/{provider}-{type}-summary.csv", "a+") as f:
    #     writer = csv.writer(f)
    #     if not file_exists:
    #         writer.writerow(("timestamp", "ttl", "ip", "hostname", "asn"))
    #     writer.writerows(results)

with open(args.region_file, "r") as csvfile:
    next(csvfile)  # skipping the header
    reader = csv.reader(csvfile)

    for row in reader:
        provider, region, ip = row
        dir = args.directory
        Path(dir+"/"+provider).mkdir(parents=True, exist_ok=True)

        for p in ["ICMP", "UDP", "TCP"]:            
            dt=datetime.now().isoformat()
            results=[]

            filename = f"{dir}/{provider}/{region}-{ip}-{dt}-{p}-normal.csv"
            run_traceroute(filename,"normal")
            
            conf.route.add(net="0.0.0.0/0", gw="192.168.1.1")
            filename = f"{dir}/{provider}/{region}-{ip}-{dt}-{p}-starlink.csv"
            run_traceroute(filename,"starlink")
            conf.route.delt(net="0.0.0.0/0", gw="192.168.1.1")
    