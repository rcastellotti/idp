# simple script to check the first hop after the starlink network

from urllib.request import urlopen
import csv
import argparse
import os
import pyasn

def main(host, protocol):
    print(f"==analysing traceroute to {host} using {protocol} protocol")
    dir = "/root/idp-castellotti/traceroutes_cgs"
    for filename in os.listdir(f"{dir}/{host}"):
        with open(os.path.join(f"{dir}/{host}", filename), "r") as f:
            if filename.startswith(protocol):
                with open(f"{dir}/{host}/{filename}") as csv_file:
                    csv_reader = csv.reader(csv_file, delimiter=",")
                    for row in csv_reader:
                        print(f"hop # {row[0]} address: {row[1]}")q


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="gsc", description="check first hop after starlink"
    )
    parser.add_argument("--host", "-H", help="host")
    parser.add_argument(
        "--protocol", "-P", help="protocol", choices=["icmp", "tcp", "udp"]
    )
    args = parser.parse_args()
    main(args.host, args.protocol)
