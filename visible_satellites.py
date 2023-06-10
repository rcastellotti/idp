import time
from csv import writer
from datetime import datetime
import os
from starlink_grpc import status_data
from common import calculate_visible_satellites
import argparse


# python3 visible_satellites.py \
#     -lat 48.2489 \
#     -lon 11.6532 \
#     -el 0 \
#     -d 800 \
#     -o /home/rc/idp-castellotti-data/visible_satellites_garching.csv

# garching coordinates
observer_latitude = 48.2489
observer_longitude = 11.6532
observer_elevation = 0

parser = argparse.ArgumentParser(prog="visible_satellites")
parser.add_argument(
    "--verbose", "-v", help="verbose", action=argparse.BooleanOptionalAction
)
parser.add_argument("--latitude", "-lat", help="observer latitude", required=True, type=float)
parser.add_argument("--longitude", "-lon", help="observer longitude", required=True, type=float)
parser.add_argument("--elevation", "-el", help="observer evelation", required=True, type=float)
parser.add_argument(
    "--distance", "-d", help="max distance for satellites (km)", required=True,type=int
)
parser.add_argument("--output", "-o", help="output file", required=True)
args = parser.parse_args()

file_exists = os.path.exists(args.output)

while True:
    with open("visible_satellites.csv", "a+") as f:
        csv_writer = writer(f)
        if not file_exists:
            csv_writer.writerow(
                [
                    "timestamp",
                    "satellite_norad",
                    "satellite",
                    "alt",
                    "az",
                    "pop_ping_latency_ms",
                ]
            )
        satellites = calculate_visible_satellites(
            args.latitude, args.longitude, args.elevation, args.distance
        )
        for sat, alt, az in satellites:
            pop_ping_latency_ms = status_data()[0]["pop_ping_latency_ms"]
            row = [
                datetime.now(),
                sat.model.satnum,
                sat.name,
                alt,
                az,
                pop_ping_latency_ms,
            ]
            csv_writer.writerow(row)
            print(row)
    time.sleep(60)
