# simple script to check the first hop after the starlink network, uses result from `check_ground_station.sh`

import csv
import argparse
import os
import pyasn

asndb = pyasn.pyasn("/root/idp-castellotti-data/ipasn_20230315.dat")


def main(host, protocol):
    print(f"==analysing traceroute to {host} using {protocol} protocol")
    dir = f"/root/idp-castellotti-data/traceroutes_cgs/{host}"
    for filename in os.listdir(dir):
        with open(os.path.join(dir, filename), "r") as f:
            if filename.startswith(protocol):
                with open(f"{dir}/{filename}") as csv_file:
                    csv_reader = csv.reader(csv_file, delimiter=",")
                    for row in csv_reader:
                        if row[1] != "*":
                            lookup = asndb.lookup(row[1])
                            # first hop after starlink
                            if lookup[0] != 14593 and lookup[0] is not None:
                                print(os.path.abspath(f.name))
                                print(f"hop #{row[0]} ip: {row[1]} ==> {lookup}")
                                break
                    print("\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="gsc", description="check first hop after starlink"
    )
    parser.add_argument(
        "--host",
        "-H",
        help="host",
        choices=["utu.fi", "caida.org", "tum.de", "garr.it", "mit.edu", "unibuc.ro","ox.ac.uk","cam.ac.uk","www.uct.ac.za"],
    )
    parser.add_argument(
        "--protocol", "-P", help="protocol", choices=["icmp", "tcp", "udp"]
    )
    args = parser.parse_args()
    main(args.host, args.protocol)
