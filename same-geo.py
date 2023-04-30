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

# use starlink
conf.route.add(net="0.0.0.0/0", gw="192.168.1.1")


parser = argparse.ArgumentParser(
    prog="reach-single-target",
    description="reach the same target overtime and saves the hops related to starlink",
)
parser.add_argument(
    "--verbose", "-v", help="verbose", action=argparse.BooleanOptionalAction
)
parser.add_argument(
    "--download", help="download file https://www.gstatic.com/ipranges/cloud.json"
)
parser.add_argument(
    "--asndb", help="asndb file location"
)
parser.add_argument("--directory", "-d", help="where to store files", required=True)
args = parser.parse_args()  

if args.download:
    urllib.request.urlretrieve(
        "https://www.gstatic.com/ipranges/cloud.json", "cloud.json"
    )

if args.verbose:
    logging.getLogger().setLevel(logging.DEBUG)
    logging.getLogger("urllib3").setLevel(logging.WARNING)

else:
    logging.getLogger().setLevel(logging.INFO)


targets = [
    {
        "area": "it",
        "data": [
            {
                "region": "europe-west8",
                "name": "milan",
                "prefix": "34.0.160.0/19",
            },
            {
                "region": "europe-west12",
                "name": "turin",
                "prefix": "34.17.0.0/16",
            },
        ],
    },
    {
        "area": "jp",
        "data": [
            {
                "area": "jp",
                "region": "asia-northeast1",
                "name": "tokio",
                "prefix": "34.17.0.0/16",
            },
            {
                "area": "jp",
                "region": "asia-northeast2",
                "name": "osaka",
                "prefix": "34.127.177.0/24",
            },
        ],
    },
    {
        "area": "us",
        "data": [
            {
                "area": "us",
                "region": "us-west-2",
                "name": "los-angeles",
                "prefix": "34.20.128.0/17",
            },
            {
                "area": "us",
                "region": "us-west-4",
                "name": "las-vegas",
                "prefix": "34.16.128.0/17",
            },
        ],
    },
]

for t in targets:
    area = t["area"]
    data = t["data"]
    dir=f"{args.directory}/{area}"
    logging.debug({dir})

    Path(dir).mkdir(parents=True, exist_ok=True)
    for i in data:
        region=i["region"]
        name=i["name"]
        prefix=i["prefix"]
        ips = [str(ip) for ip in IPv4Network(prefix)]
        random_ip_address = random.choice(ips)
        logging.debug(f"{dir}/{region}-{name}")
        reach_target(random_ip_address,f"{dir}/{region}-{name}-{random_ip_address}",args.asndb)