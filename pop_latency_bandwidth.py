"""
get popPingLatencyMs and downlinkThroughputBps from the get_status endpoint
"""

import csv
import json
import argparse
import logging
import time

from datetime import datetime
from api import get_status

parser = argparse.ArgumentParser(
    prog="extract latency and bandwidth over a period of time"
)
parser.add_argument(
    "--verbose", "-v", help="verbose", action=argparse.BooleanOptionalAction
)
parser.add_argument("--output", "-o", help="output filename", required=True, type=str)
parser.add_argument(
    "--interval",
    "-i",
    help="how long should the measurement run for",
    required=True,
    type=int,
)


def main():
    with open(args.output, "a", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(("timestamp", "pop_ping_latency_ms", "downlinkThroughputBps"))

        while True:
            s = json.loads(get_status())
            lat = s["dishGetStatus"]["popPingLatencyMs"]
            bw = s["dishGetStatus"]["downlinkThroughputBps"]

            writer.writerow([datetime.now(), lat, bw])
            f.flush()
            time.sleep(args.interval)


if __name__ == "__main__":
    args = parser.parse_args()
    if args.verbose:
        logging.basicConfig(level="INFO")
    main()
