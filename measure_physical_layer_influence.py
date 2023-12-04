"""
measure pop ping latency and rtt while running iperf, usage examples:
+ python3 measure_physical_layer_influcence -b 10K
+ iperf3 -c TARGET -u -b 10K -t 3600

+ python3 measure_physical_layer_influcence -b 20K
+ iperf3 -c TARGET -u -b 20K -t 3600

+ python3 measure_physical_layer_influcence -b 50K
+ iperf3 -c TARGET -u -b 50K -t 3600

+ python3 measure_physical_layer_influcence -b 100K
+ iperf3 -c TARGET -u -b 100K -t 3600

+ python3 measure_physical_layer_influcence -b 1M
+ iperf3 -c TARGET -u -b 1M -t 3600

+ python3 measure_physical_layer_influcence -b 10M
+ iperf3 -c TARGET -u -b 10M -t 3600
remeber to set a route to use starlink when reaching the target
"""
import csv
import time
import argparse
import os
import json
from scapy.layers.inet import IP, ICMP
from scapy.sendrecv import sr1
from scapy.config import conf
from api import get_status


parser = argparse.ArgumentParser(
    prog="measure pop_ping_latency and rtt with iperf running"
)
parser.add_argument("--bandwidth", "-b", help="bandwidth", required=True)
args = parser.parse_args()

conf.route.add(net="0.0.0.0/0", gw="192.168.1.1")


def measure():
    """
    run the measurement, remember to run iperf in the background
    """
    filename = f"./pli-{args.bandwidth}.csv"
    file_exists = os.path.isfile(filename)
    with open(filename, "a", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(("timestamp", "rtt", "pop_ping_latency_ms"))
        probe_timestamp = int(time.time())
        # this is the first hop after starlink network we are seeing often
        pkt = IP(dst="213.144.184.30") / ICMP()
        reply = sr1(pkt, verbose=False, timeout=1)
        if reply is not None:
            rtt_ms = (reply.time - pkt.sent_time) * 1000
            time.sleep(1)
            print([probe_timestamp, rtt_ms])
            status = json.loads(get_status())["dishGetStatus"]
            pop_ping_latency_ms = status["popPingLatencyMs"]
            writer.writerow([probe_timestamp, rtt_ms, pop_ping_latency_ms])


t_end = time.time() + 60 * 5
while time.time() < t_end:
    measure()

conf.route.delt(net="0.0.0.0/0", gw="192.168.1.1")
