import psutil
import time
from starlink_grpc import status_data
import warnings
import logging
import csv
import os
from datetime import datetime
from common import read_rx_bytes
warnings.filterwarnings("ignore")

# remember to while true; do wget -4 https://speed.hetzner.de/10GB.bin --report-speed=bits -O /dev/null; done
# sudo ip route add 88.198.248.254  via 192.168.1.1

interface="enp1s0f3"
filename="large_file_download_3parallel.csv"
file_exists = os.path.exists(filename)
with open(filename, "a+") as f:
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
with open(filename, "a") as f:
    csv_writer = csv.writer(f)
    while True:
        time.sleep(1)
        current_bytes = read_rx_bytes(interface)
        bandwidth = (current_bytes-previous_bytes)*8
        previous_bytes = current_bytes
        pop_ping_latency_ms = status_data()[0]["pop_ping_latency_ms"]
        downlink_throughput_bps = status_data()[0]["downlink_throughput_bps"]
        csv_writer.writerow(
            [
                datetime.now(),
                bandwidth,
                pop_ping_latency_ms,
                downlink_throughput_bps,
            ]
        )
