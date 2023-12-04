"""
Measure bandwidth from the sys/class/net/{interface}/statistics/rx_bytes
Linux file and compare it with the values from the api,
The interface is hardcoded, of course it is Starlink's interface
Sample usage:
python3 measure_bandwidth.py -o test_bandwidth.csv
"""
import csv
import json
import logging
import os
import time
import argparse
from api import get_status

parser = argparse.ArgumentParser(prog="map")
parser.add_argument(
    "--verbose", "-v", help="verbose", action=argparse.BooleanOptionalAction
)
parser.add_argument("--output_file", "-o", help="output file", required=True, type=str)
parser.add_argument(
    "--interval",
    "-interval",
    help="how long should the measurement run for",
    required=True,
    type=int,
)
args = parser.parse_args()
directory = args.directory


def read_rx_bytes(interface):
    """
    Read bytes received from `interface`
    """
    with open(
        f"/sys/class/net/{interface}/statistics/rx_bytes", "r", encoding="utf-8"
    ) as file:
        rx_bytes = int(file.read())
    return rx_bytes


def main(filename):
    """
    Get bandwidth from the api

    """
    interface = "enp1s0f3"
    file_exists = os.path.exists(filename)
    with open(filename, "a+", encoding="utf-8") as f:
        csv_writer = csv.writer(f)
        if not file_exists:
            csv_writer.writerow(
                [
                    "timestamp",
                    "bandwidth_bps",
                    "pop_ping_latency_ms",
                    "downlink_troughput_bps",
                ]
            )

    previous_bytes = read_rx_bytes(interface)
    with open(filename, "a", encoding="utf-8") as f:
        csv_writer = csv.writer(f)
        while True:
            time.sleep(1)
            current_bytes = read_rx_bytes(interface)
            bandwidth = (current_bytes - previous_bytes) * 8
            previous_bytes = current_bytes
            status = json.loads(get_status())["dishGetStatus"]
            pop_ping_latency_ms = status["popPingLatencyMs"]
            downlink_throughput_bps = status["downlinkThroughputBps"]
            csv_writer.writerow(
                [
                    int(time.time()),
                    bandwidth,
                    pop_ping_latency_ms,
                    downlink_throughput_bps,
                ]
            )
            f.flush()


if __name__ == "__main__":
    args = parser.parse_args()
    if args.verbose:
        logging.basicConfig(level="INFO")
    main(args.output_file)
