"""
this module offers common functions, namely:
"""
import csv
import logging
import json
import os
from datetime import datetime
import socket
import time
import pyasn
from scapy.layers.inet import IP, UDP, TCP, ICMP
from scapy.sendrecv import sr1
from skyfield.api import Topos, load
from api import get_status


def read_rx_bytes(interface):
    """
    read bytes received from `interface`
    """
    with open(
        f"/sys/class/net/{interface}/statistics/rx_bytes", "r", encoding="utf-8"
    ) as file:
        rx_bytes = int(file.read())
    return rx_bytes


def reach_target(target, filename, asndb):
    """
    this function reaches a target and saves HOPS related to Starlink
    in a csv file
    """
    asndb = pyasn.pyasn(asndb)
    time_now = datetime.now()
    filename = f"{filename}.csv"
    file_exists = os.path.isfile(filename)
    with open(filename, "a", encoding="utf-8") as f:
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
                    writer.writerow([time_now, i, src])


# i should turn this into a class with a .run() method and a .display() method
def traceroute(target, protocol, asndb):
    """
    + traceroute("1.1.1.1","ICMP", "../idp-castellotti-data/ipasn_20230315.dat")
    + traceroute("1.1.1.1","UDP", "../idp-castellotti-data/ipasn_20230315.dat")
    + traceroute("1.1.1.1","TCP", "../idp-castellotti-data/ipasn_20230315.dat")
    """
    asndb = pyasn.pyasn(asndb)

    ttl = 1
    probe_timestamp = int(time.time())
    results = []
    while ttl < 30:
        pkt_base = IP(dst=target, ttl=ttl)
        pkt = ""
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


def calculate_visible_satellites(
    observer_latitude, observer_longitude, observer_elevation, distance_km
):
    """
    calculate visible satellites using skyfield
    """
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


# remember to while true; do wget -4 https://speed.hetzner.de/10GB.bin
#             --report-speed=bits -O /dev/null; done
# sudo ip route add 88.198.248.254  via 192.168.1.1
def measure_bw(filename):
    """
    get bandwidth from the api

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
