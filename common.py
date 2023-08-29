# common stuff used in different scripts
import csv
import logging
import json
import os
from datetime import datetime
import socket
import numpy as np
import time
import re
import matplotlib.pyplot as plt
from ipaddress import ip_address, IPv4Address, IPv6Address

from nine981 import get_status
import pyasn
from scapy.all import (
    IP,
    TCP,
    IPv6,
    conf,
    ICMP,
    sr1,
    UDP,
)
from pathlib import Path
from skyfield.api import Topos, load

import re

def is_ipv4(address):
    ipv4_pattern = r'^(\d{1,3}\.){3}\d{1,3}$'
    return re.match(ipv4_pattern, address) is not None

def is_ipv6(address):
    ipv6_pattern = r'^([0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}$'
    return re.match(ipv6_pattern, address) is not None

def read_rx_bytes(interface):
    with open(f"/sys/class/net/{interface}/statistics/rx_bytes", "r") as file:
        rx_bytes = int(file.read())
    return rx_bytes


def reach_target(target, filename, asndb):
    """
    this function reaches a target and saves HOPS related to Starlink
    in a csv file
    """
    asndb = pyasn.pyasn(asndb)
    time = datetime.now()
    filename = f"{filename}.csv"
    file_exists = os.path.isfile(filename)
    f = open(filename, "a")
    writer = csv.writer(f)
    if not file_exists:
        writer.writerow(["time", "hop#", "ip"])
    for i in range(3, 8):
        pkt = IP(dst=target, ttl=i) / ICMP()
        res = sr1(pkt, verbose=0, timeout=3)
        if res:
            src = res.src
            logging.debug(src)
            lookup = asndb.lookup(src)
            if lookup[0] == 14593:
                writer.writerow([time, i, src])


# i should turn this into a class with a .run() method and a .display() method
def traceroute(target, protocol, asndb):
    asndb = pyasn.pyasn(asndb)

    ttl = 1
    probe_timestamp = int(time.time())
    results = []
    while ttl < 30:
        if  is_ipv6(target):
            pkt_base = IPv6(dst=target, hlim=ttl)
        elif is_ipv4(target):
            pkt_base = IP(dst=target, ttl=ttl)


        if protocol == "ICMP":
            pkt = pkt_base / ICMP()
        elif protocol == "UDP":
            pkt = pkt_base / UDP(dport=53)
        elif protocol == "TCP":
            pkt = pkt_base / TCP(dport=80, flags="S")
        reply = sr1(pkt, verbose=False, timeout=1)
        if reply is None:
            results.append([probe_timestamp, ttl, "*", "*", "*", "*"])
            ttl += 1
        else:
            hostname = ""
            try:
                hostname = socket.gethostbyaddr(reply.src)[0]
            except socket.herror:
                hostname = "???"
            asn = asndb.lookup(reply.src)[0]
            rtt_ms = (reply.time - pkt.sent_time) * 1000

            r = (probe_timestamp, ttl, reply.src, hostname, asn, rtt_ms)
            results.append(r)

            if (
                protocol == "ICMP"
                and reply.type == 0
                or protocol == "UDP"
                and reply.type == 3
                or protocol == "TCP"
                and reply.haslayer(TCP)
                and reply.getlayer(TCP).flags == "SA"
            ):
                break
            ttl += 1
    return results


def run_traceroute_and_save_to_file(filename, ip, protocol, asndb):
    logging.debug(f"traceroute: {filename}")
    file_exists = os.path.isfile(filename)
    with open(filename, "a") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(("timestamp", "hop", "ip", "hostname", "asn", "rtt"))
        results = traceroute(ip, protocol, asndb=asndb)
        writer.writerows(results)


# def cloud_traceroutes(region_file, output_directory, asndb):
#     with open(region_file, "r") as csvfile:
#         next(csvfile)  # skipping the header
#         reader = csv.reader(csvfile)

#         for row in reader:
#             provider, region, ip = row
#             dir = output_directory
#             Path(dir + "/" + provider).mkdir(parents=True, exist_ok=True)

#             # for protocol in ["ICMP", "UDP", "TCP"]:
#             for protocol in ["ICMP"]:
#                 dt = datetime.datetime.now().isoformat()
#                 # normal
#                 filename = f"{dir}/{provider}/{region}-{ip}-{dt}-{protocol}-normal.csv"
#                 run_traceroute_and_save_to_file(filename, ip, protocol, asndb)
#                 # starlink
#                 conf.route.add(net="0.0.0.0/0", gw="192.168.1.1")
#                 filename = (
#                     f"{dir}/{provider}/{region}-{ip}-{dt}-{protocol}-starlink.csv"
#                 )
#                 run_traceroute_and_save_to_file(filename, ip, protocol, asndb)
#                 conf.route.delt(net="0.0.0.0/0", gw="192.168.1.1")


def calculate_visible_satellites(
    observer_latitude, observer_longitude, observer_elevation, distance_km
):
    stations_url = (
        "https://celestrak.org/NORAD/elements/gp.php?GROUP=starlink&FORMAT=tle"
    )

    satellites = load.tle_file(stations_url)
    observer = Topos(observer_latitude, observer_longitude, observer_elevation)
    ts = load.timescale()
    t = ts.now()

    # Calculate satellite positions
    positions = []
    for sat in satellites:
        satellite = sat
        position = (satellite - observer).at(t)
        positions.append((sat, position))

    # Filter visible satellites
    visible_satellites = []
    for sat, position in positions:
        alt, az, distance = position.altaz()
        # Satellite is above the horizon
        if alt.degrees > 0 and distance.km < distance_km:
            visible_satellites.append((sat, alt, az))

    return visible_satellites


def extract_between_dash_and_json(input_string):
    pattern = r"map-(.*).json"
    match = re.search(pattern, input_string)
    if match:
        return match.group(1)
    else:
        return None


def detect_handovers(dir):
    l = sorted(os.listdir(dir))
    last=0
    print(
        f"[*] examining obstruction maps in interval: {l[0][:-4]} and {extract_between_dash_and_json(l[-1][:-4])}"
    )
    suspected_handovers = []
    for i in range(0, len(l) - 1, 2):
        
        f1 = os.path.join(dir, l[i])
        f2 = os.path.join(dir, l[i + 1])
        fv1 = os.path.join(dir + "-viz", l[i]) + ".png"
        os.path.join(dir + "-viz", l[i + 1]) + ".png"

        map1 = json.load(open(f1))
        map1 = map1["dishGetObstructionMap"]["snr"]
        map1 = np.array(map1).reshape(123, 123)
        map2 = json.load(open(f2))
        map2 = map2["dishGetObstructionMap"]["snr"]
        map2 = np.array(map2).reshape(123, 123)

        new_map = map1 + map2
        new_dots = np.count_nonzero(new_map == 0)
        if new_dots > 0:
            x, y = np.where(new_map == 0)
            for hx in x:
                for hy in y:
                    pot = new_map[hx - 1 : hx + 2, hy - 1 : hy + 2]
                    if 2 not in pot:
                        new_t=extract_between_dash_and_json(fv1)
                        # print(
                        #         f"[-] handover detected: {new_t} rel: {(datetime.fromtimestamp(float(new_t))-datetime.fromtimestamp(float(last))).total_seconds()} "
                    
                        # )
                        suspected_handovers.append(new_t)
            last=extract_between_dash_and_json(fv1)
    return suspected_handovers 


# remember to while true; do wget -4 https://speed.hetzner.de/10GB.bin --report-speed=bits -O /dev/null; done
# sudo ip route add 88.198.248.254  via 192.168.1.1
def measure_bw(filename):
    interface="enp1s0f3"
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
            status=json.loads(get_status())["dishGetStatus"]
            # print(status)
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


def visualize_handover(f1,f2):
    fig, ax = plt.subplots(1, 2,figsize=(12,7))
    map1 = json.load(open(f1))
    map1 = map1["dishGetObstructionMap"]["snr"]
    map1 = np.array(map1).reshape(123, 123)
    map2 = json.load(open(f2))
    map2 = map2["dishGetObstructionMap"]["snr"]
    map2 = np.array(map2).reshape(123, 123)
    ax[0].imshow(map1)
    ax[1].imshow(map2)
    plt.title(f"{f1} ~> {f2}")
    plt.plot()


def detect_handovers(f1,f2,lista):
    map1 = json.load(open(f1))
    map1 = map1["dishGetObstructionMap"]["snr"]
    map1 = np.array(map1).reshape(123, 123)

    map2 = json.load(open(f2))
    map2 = map2["dishGetObstructionMap"]["snr"]
    map2 = np.array(map2).reshape(123, 123)
    
    new=map1+map2

    rows, cols = np.where(new == 0)
    zero_coordinates = list(zip(rows, cols))
    for coord in zero_coordinates:
        #     print(coord)
        hx=coord[0]
        hy=coord[1]
        pot = new[hx - 2 : hx + 2, hy - 2 : hy + 2]
        if not 2 in pot:
            head, tail = os.path.split(f1)
            lista.append(int(tail[:-5]))
            # logging.info(f"detected handover between {f1} and {f2}")