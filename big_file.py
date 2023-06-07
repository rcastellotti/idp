import psutil
import time
from starlink_grpc import status_data
import warnings
import logging
import csv
import os
from datetime import datetime

warnings.filterwarnings("ignore")


## remember to run rc@gnolmir ~/idp-castellotti (main)> wget -4 https://speed.hetzner.de/10GB.bin --report-speed=bits -O /dev/null
# and to set appropriately the route!!!!


# https://stackoverflow.com/a/62020919
def net_usage(inf="enp1s0f2"):  # change the inf variable according to the interface
    net_stat = psutil.net_io_counters(pernic=True, nowrap=True)[inf]
    net_in_1 = net_stat.bytes_recv
    net_out_1 = net_stat.bytes_sent
    time.sleep(1)
    net_stat = psutil.net_io_counters(pernic=True, nowrap=True)[inf]
    net_in_2 = net_stat.bytes_recv
    net_out_2 = net_stat.bytes_sent

    net_in = (net_in_2 - net_in_1) / 1024/1024
    net_out = (net_out_2 - net_out_1) / 1024 /1024

    logging.info(f"IN: {net_in} MB/s, OUT: {net_out} MB/s")
    return net_in, net_out


file_exists = os.path.exists("large_file_download.csv")
with open("large_file_download.csv", "a+") as f:
    csv_writer = csv.writer(f)
    if not file_exists:
        csv_writer.writerow(
            [
                "timestamp",
                "net_in_mbps",
                "net_out_mbps",
                "pop_ping_latency_ms",
                "downlink_troughput_bps",
            ]
        )
while True:
    with open("large_file_download.csv", "a") as f:
        csv_writer = csv.writer(f)

        net_in, net_out = net_usage()
        pop_ping_latency_ms = status_data()[0]["pop_ping_latency_ms"]
        downlink_throughput_bps = status_data()[0]["downlink_throughput_bps"] / 1024
        print(net_in, net_out, pop_ping_latency_ms, downlink_throughput_bps)
        csv_writer.writerow(
            [
                datetime.now(),
                net_in,
                net_out,
                pop_ping_latency_ms,
                downlink_throughput_bps,
            ]
        )
