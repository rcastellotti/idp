import csv
import os
import time
from scapy.all import (
    conf,
    ICMP,
    IP,
    sr1,
)
from starlink_grpc import status_data
import argparse

parser = argparse.ArgumentParser(prog="pop_ping_latency with iperf running")

parser.add_argument("--bandwidth", "-b", help="bandwidth", required=True)

args = parser.parse_args()
conf.route.add(net="0.0.0.0/0", gw="192.168.1.1")


def ping(bw):
    filename = f"./ping-bw-{args.bandwidth}.csv"
    file_exists = os.path.isfile(filename)

    with open(filename, "a") as f:
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
            writer.writerow(
                [probe_timestamp, rtt_ms, status_data()[0]["pop_ping_latency_ms"]]
            )


t_end = time.time() + 60 * 5
while time.time() < t_end:
    ping("normal")
conf.route.delt(net="0.0.0.0/0", gw="192.168.1.1")
