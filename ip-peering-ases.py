# this data comes from https://publicdata.caida.org/datasets/as-relationships/serial-1/20230401.as-rel.txt.bz2
# produces a file containing a list of hostnames belonging to each as

# sample usage:
#   python3 ip-peering-ases.py \
#       --ases 10 --prefix 5 --ips 5 \
#       -i ../idp-castellotti-data/20230401.as-rel.txt \
#       -o ../idp-castellotti-data/ip-peering-ases.json

import csv
import argparse
import requests
import json
from ipaddress import IPv4Network
import random
import socket
from tqdm import tqdm
import logging
from pygments import highlight, lexers, formatters

csv.register_dialect("piper", delimiter="|", quoting=csv.QUOTE_NONE)

parser = argparse.ArgumentParser(prog="parse", description="caidastuff helper")
parser.add_argument("--input", "-i", help="input", required=True)
parser.add_argument("--output", "-o", help="output", required=True)
parser.add_argument(
    "--ases", "-a", help="number of ases to sample", required=True, type=int
)
parser.add_argument(
    "--prefix", "-p", help="number of prefixes", required=True, type=int
)
parser.add_argument("--ips", "-j", help="number of ips", required=True, type=int)
parser.add_argument(
    "--verbose", "-v", help="verbose", action=argparse.BooleanOptionalAction
)
args = parser.parse_args()
if args.verbose:
    logging.getLogger().setLevel(logging.DEBUG)
else:
    logging.getLogger().setLevel(logging.INFO)

# getting all ASes peering with SpaceX (AS14593)
ases=[]
with open(args.input, "r") as csvfile:
    for row in csv.reader(csvfile, dialect="piper"):
        if row[2] == "0":
            if row[0] != "14593":
                ases.append(row[0])
            else:
                ases.append(row[1])

# getting as names, prefixes and random ips from certain ases
ases_ip = []
ases = random.choices(ases, k=args.ases)
for _as in ases:
    r = requests.get("https://stat.ripe.net/data/as-names/data.json", params={"resource":_as})
    asname = r.json()["data"]["names"][_as]
    url = "https://stat.ripe.net/data/announced-prefixes/data.json"
    params = {"resource": _as, "starttime": "2020-12-12T12:00"}
    r = requests.get(url, params=params)
    j = r.json()
    prefixes = j["data"]["prefixes"]
    prefixes = random.choices(prefixes, k=args.prefix)
    formatted_json = json.dumps(j, indent=4)
    colorful_json = highlight(
        formatted_json, lexers.JsonLexer(), formatters.TerminalFormatter()
    )
    logging.debug()
    logging.info(f"ASN: {_as}")
    for prefix in tqdm(prefixes):
        p = prefix["prefix"]
        if ":" not in p:
            logging.debug(f"network: {p}")
            ips = [str(ip) for ip in IPv4Network(p)]
            ips = random.choices(ips, k=args.ips)
            logging.debug(f"random ips: {ips}")
            hostnames = [socket.getnameinfo((ip, 0), 0)[0] for ip in ips]
            logging.debug(f"hostnames: {hostnames}")
            tmp = dict()
            tmp["asn"] = _as
            tmp["as_name"] = asname
            tmp["ips"] = ips
            tmp["hostnames"] = hostnames
            ases_ip.append(tmp)

with open(args.output, "w") as f:
    json.dump(ases_ip, f)
