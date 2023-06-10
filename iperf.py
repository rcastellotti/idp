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

conf.route.add(net="0.0.0.0/0", gw="192.168.1.1")


def ping(bw):
    filename = f"./ping-bw-{bw}.csv"
    file_exists = os.path.isfile(filename)

    with open(filename, "a") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(("timestamp", "rtt", "pop_ping_latency_ms"))
        probe_timestamp = int(time.time())
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
