"""
this module offers common functions
"""
import socket
import os
import time
import json
import pyasn
import numpy as np
from skyfield.api import Topos, load


def get_adjacent_files(directory_path):
    """
    creates list of tuples of adjacent files, used to detect handovers
    """
    file_list = sorted(os.listdir(directory_path))
    couples = []
    for i in range(len(file_list) - 1):
        current_file = file_list[i]
        next_file = file_list[i + 1]
        couples.append((current_file, next_file))
    return couples


def detect_handovers(f1, f2):
    """
    check whether an handover happened between two obstruction maps
    """
    map1 = json.load(open(f1))
    map1 = map1["dishGetObstructionMap"]["snr"]
    map1 = np.array(map1).reshape(123, 123)

    map2 = json.load(open(f2))
    map2 = map2["dishGetObstructionMap"]["snr"]
    map2 = np.array(map2).reshape(123, 123)

    new = map1 + map2

    rows, cols = np.where(new == 0)
    zero_coordinates = list(zip(rows, cols))
    for coord in zero_coordinates:
        hx = coord[0]
        hy = coord[1]
        pot = new[hx - 2 : hx + 2, hy - 2 : hy + 2]
        if 2 not in pot:
            # print(f"detected handover between {f1} and {f2}")
            head, tail = os.path.split(f1)
            return int(tail[:-5])
        return None


def traceroute(target, protocol, asndb):
    """
    + traceroute("1.1.1.1","ICMP", "../idp-castellotti-data/ipasn_20230315.dat")
    + traceroute("1.1.1.1","UDP", "../idp-castellotti-data/ipasn_20230315.dat")
    + traceroute("1.1.1.1","TCP", "../idp-castellotti-data/ipasn_20230315.dat")
    """
    # believe it or not, this is valid
    from scapy.layers.inet import IP, UDP, TCP, ICMP
    from scapy.sendrecv import sr1

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
