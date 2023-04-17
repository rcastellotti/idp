# this data comes from https://publicdata.caida.org/datasets/as-relationships/serial-1/20230401.as-rel.txt.bz2
# produces a file containing a list of hostnames belonging to each as
# number of prefixes is configurable

# TODO: download the file and clear it automatically

# sample usage:
#   python3 ip-peering-ases.py \
#       --ases 10 --prefix 5  \
#       -i ../idp-castellotti-data/20230401.as-rel.txt \
#       -o ../idp-castellotti-data/ip-peering-ases.csv

import csv
import argparse
import requests
import json
from ipaddress import IPv4Network
import random
import socket
from tqdm import tqdm
import logging

csv.register_dialect("piper", delimiter="|", quoting=csv.QUOTE_NONE)

parser = argparse.ArgumentParser(
    prog="parse", description="extract ips from ases peering with spacex"
)
parser.add_argument("--input", "-i", help="input", required=True)
parser.add_argument("--output", "-o", help="output", required=True)
parser.add_argument(
    "--ases", "-a", help="number of ases to sample", required=True, type=int
)
parser.add_argument(
    "--prefix", "-p", help="number of prefixes", required=True, type=int
)
parser.add_argument(
    "--verbose", "-v", help="verbose", action=argparse.BooleanOptionalAction
)
args = parser.parse_args()
if args.verbose:
    logging.getLogger().setLevel(logging.DEBUG)
    logging.getLogger("urllib3").setLevel(logging.WARNING)

else:
    logging.getLogger().setLevel(logging.INFO)

# getting all ASes peering with SpaceX (AS14593)
ases = set()
with open(args.input, "r") as csvfile:
    for row in csv.reader(csvfile, dialect="piper"):
        if row[2] == "0":
            if row[0] != "14593":
                ases.add(row[0])
            else:
                ases.add(row[1])

# getting as names, prefixes and random ips from certain ases
ases_list = random.choices(list(ases), k=args.ases)

with open(args.output, "a") as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(["asn", "asname", "prefix", "ip", "hostname"])

for _as in ases_list:
    r = requests.get(
        "https://stat.ripe.net/data/as-names/data.json", params={"resource": _as}
    )
    asname = r.json()["data"]["names"][_as]

    r = requests.get(
        "https://stat.ripe.net/data/announced-prefixes/data.json",
        params={"resource": _as, "starttime": "2023-04-01T12:00"},
    )
    j = r.json()
    prefixes = j["data"]["prefixes"]

    # this is needed because some ases announce just a few prefixes (<5)
    number_of_prefixes = min(len(prefixes) - 1, args.prefix)
    prefixes = random.choices(prefixes, k=number_of_prefixes)
    logging.info(f"ASN: {_as}")

    for prefix in tqdm(prefixes):
        prefix = prefix["prefix"]
        if ":" not in prefix:
            logging.debug(f"network: {prefix}")
            ips = [str(ip) for ip in IPv4Network(prefix)]
            ip = random.choice(ips)
            try:
                hostname = socket.getnameinfo((ip, 0), 0)[0]
            except:
                pass
            logging.debug(f"hostname: {hostname}")
            with open(args.output, "a") as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow([_as, asname, prefix, ip, hostname])
