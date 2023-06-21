import psutil
import time
from starlink_grpc import status_data
import warnings
import logging
import csv
import os
from datetime import datetime
from common import read_rx_bytes,calculate_bandwidth
warnings.filterwarnings("ignore")


## remember to run rc@gnolmir ~/idp-castellotti (main)> wget -4 https://speed.hetzner.de/10GB.bin --report-speed=bits -O /dev/null
# and to set appropriately the route!!!!

interface="enp1s0f3"

def monitor_bandwidth(interface, interval=1):
    previous_bytes = read_rx_bytes(interface)
    
    while True:
        time.sleep(interval)
        current_bytes = read_rx_bytes(interface)
        elapsed_time = interval
        
        bandwidth = calculate_bandwidth(previous_bytes, current_bytes, elapsed_time)
        previous_bytes = current_bytes
        
        print(f'Bandwidth: {bandwidth:.2f} bytes/s')

        

file_exists = os.path.exists("large_file_download.csv")
with open("large_file_download.csv", "a+") as f:
    csv_writer = csv.writer(f)
    if not file_exists:
        csv_writer.writerow(
            [
                "timestamp",
                "bandwidth_Bps",
                "pop_ping_latency_ms",
                "downlink_troughput_bps",
            ]
        )
    
previous_bytes = read_rx_bytes(interface)

with open("large_file_download.csv", "a") as f:
    csv_writer = csv.writer(f)

    while True:
        time.sleep(1)
        current_bytes = read_rx_bytes(interface)
        elapsed_time = 1
        
        bandwidth = calculate_bandwidth(previous_bytes, current_bytes, elapsed_time)
        previous_bytes = current_bytes
        
       
        pop_ping_latency_ms = status_data()[0]["pop_ping_latency_ms"]
        downlink_throughput_bps = status_data()[0]["downlink_throughput_bps"] / 1024
        print(bandwidth, pop_ping_latency_ms, downlink_throughput_bps)
        csv_writer.writerow(
            [
                datetime.now(),
                bandwidth,
                pop_ping_latency_ms,
                downlink_throughput_bps,
            ]
        )
