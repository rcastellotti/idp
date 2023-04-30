# this script tries to reach targets in the same geographic area

from scapy.all import *
import logging
import argparse
import csv
from datetime import datetime
import json
from pathlib import Path
import urllib.request
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
    "--download", "-d", help="download file https://www.gstatic.com/ipranges/cloud.json"
)
args = parser.parse_args()

if args.download:
    urllib.request.urlretrieve("https://www.gstatic.com/ipranges/cloud.json", "cloud.json")


if args.verbose:
    logging.getLogger().setLevel(logging.DEBUG)
    logging.getLogger("urllib3").setLevel(logging.WARNING)

else:
    logging.getLogger().setLevel(logging.INFO)



datacenters=[]

with open("cloud.json","r") as f:
    data=json.load(f)
    for prefix in data["prefixes"]:
        datacenters.append(prefix)


print(datacenters)
# # this script tries to reach the same target overtime and saves the hops related to starlink
# from scapy.all import *
# # import pyasn
# import logging
# import argparse
# import csv
# from datetime import datetime
# import os
# from pathlib import Path
# import json
# # use starlink
# conf.route.add(net="0.0.0.0/0", gw="192.168.1.1")

# 


# # for prefix in tqdm(prefixes):
# # prefix = prefix["prefix"]
# # if ":" not in prefix:
# #     logging.debug(f"network: {prefix}")
# #     ips = [str(ip) for ip in IPv4Network(prefix)]
# #     ip = random.choice(ips)
# #     try:
# #         hostname = socket.getnameinfo((ip, 0), 0)[0]
# #     except:
# #         pass
# #     logging.debug(f"hostname: {hostname}")
# #     with open(args.output, "a") as csv_file:
# #         writer = csv.writer(csv_file)
# #         writer.writerow([_as, asname, prefix, ip, hostname])



# parser = argparse.ArgumentParser(
#     prog="reach-single-target",
#     description="reach the same target overtime and saves the hops related to starlink",
# )
# parser.add_argument(
#     "--verbose", "-v", help="verbose", action=argparse.BooleanOptionalAction
# )

# args = parser.parse_args()


# # if args.verbose:
# #     logging.getLogger().setLevel(logging.DEBUG)
# #     logging.getLogger("urllib3").setLevel(logging.WARNING)

# # else:
# #     logging.getLogger().setLevel(logging.INFO)

# # for t in targets:
# #     logging.debug(f"reaching {t}")
# #     time = datetime.now()
# #     Path(args.directory).mkdir(parents=True, exist_ok=True)
# #     filename=f"{args.directory}/{t}.csv"
# #     file_exists=os.path.isfile(filename)
# #     f=open(filename, "a")
# #     writer = csv.writer(f)
# #     if not file_exists:
# #         writer.writerow(["time", "hop#", "ip"])

# #     for i in range(4,6):
# #         myPacket = IP(dst="www.caida.org", ttl=i) / ICMP()
# #         res = sr1(myPacket, verbose=0, timeout=3)
# #         if res:
# #             logging.debug(res.src)
# #             src = res.src
# #             lookup = asndb.lookup(src)
# #             if lookup[0] == 14593:
# #                 writer.writerow([time, i, src])
