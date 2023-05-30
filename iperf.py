# l=["10k","20k","50k","100k","1M","10M"]

# for i in l:
#     base="iperf-{i}.csv"


# import time
# import subprocess
# import threading
# import re
# def ip():
#     subprocess.call(["iperf3", "-c", "138.246.253.20" ,"-u","-b" ,"1M", "-t", "3600" ])
# def ping():
#     # ps = subprocess.Popen(('ping', '-I','enp1s0f2','213.144.184.30'), stdout=subprocess.PIPE)
#     # output = subprocess.check_output(('grep', '-Po','"time.*'), stdin=ps.stdout)
#     # ps.wait()
#     cmd = 'ping -I enp1s0f2 213.144.184.30 | grep -Po "time.*"'
#     ps = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
#     output = ps.communicate()[0]
#     print(output)

# t_end = time.time() + 60 * 15
# while time.time() < t_end:
#         # x = threading.Thread(target=ip)
#         y= threading.Thread(target=ping)
#         # x.start()
#         y.start()

import csv
import os
import subprocess
import time
import argparse
from scapy.all import (
    conf,
    ICMP,IP,
    sr1,
)
from pathlib import Path
import threading
import iperf3
from starlink_grpc import status_data

conf.route.add(net="0.0.0.0/0", gw="192.168.1.1")


def ping(bw):
    filename = f"./ping-bw-{bw}.csv"
    file_exists = os.path.isfile(filename)

    with open(filename, "a") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(("timestamp", "rtt","pop_ping_latency_ms"))
        probe_timestamp = int(time.time())
        pkt = IP(dst="213.144.184.30") / ICMP()
        reply = sr1(pkt, verbose=False, timeout=1)
        if reply is not None:
            rtt_ms = (reply.time - pkt.sent_time) * 1000
            time.sleep(1)
            print([probe_timestamp, rtt_ms])
            writer.writerow([probe_timestamp, rtt_ms,status_data()[0]["pop_ping_latency_ms"]])

t_end = time.time() + 60 * 5
while time.time() < t_end:
    ping("normal")

# t_end = time.time() + 60 * 5
# while time.time() < t_end:
#     ping("20k")

# t_end = time.time() + 60 * 5
# while time.time() < t_end:
#     ping("50k")

# t_end = time.time() + 60 * 5
# while time.time() < t_end:
#     ping("100k")

# t_end = time.time() + 60 * 5
# while time.time() < t_end:
#     ping("1M")

# t_end = time.time() + 60 * 5
# while time.time() < t_end:
#     ping("10M")

conf.route.delt(net="0.0.0.0/0", gw="192.168.1.1")
