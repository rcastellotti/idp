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
import pyasn
from scapy.all import (
    RandShort,
    sr,
    IP,
    TCP,
    RandInt,
    TracerouteResult,
    conf,
    ICMP,
    sr1,
    UDP,
)
from pathlib import Path
from skyfield.api import Topos, load


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


def cloud_traceroutes(region_file, output_directory, asndb):
    with open(region_file, "r") as csvfile:
        next(csvfile)  # skipping the header
        reader = csv.reader(csvfile)

        for row in reader:
            provider, region, ip = row
            dir = output_directory
            Path(dir + "/" + provider).mkdir(parents=True, exist_ok=True)

            # for protocol in ["ICMP", "UDP", "TCP"]:
            for protocol in ["ICMP"]:
                dt = datetime.datetime.now().isoformat()
                # normal
                filename = f"{dir}/{provider}/{region}-{ip}-{dt}-{protocol}-normal.csv"
                run_traceroute_and_save_to_file(filename, ip, protocol, asndb)
                # starlink
                conf.route.add(net="0.0.0.0/0", gw="192.168.1.1")
                filename = (
                    f"{dir}/{provider}/{region}-{ip}-{dt}-{protocol}-starlink.csv"
                )
                run_traceroute_and_save_to_file(filename, ip, protocol, asndb)
                conf.route.delt(net="0.0.0.0/0", gw="192.168.1.1")


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
        f"[*] examining obstruction maps in interval: {extract_between_dash_and_json(l[0])} and {extract_between_dash_and_json(l[-1])}"
    )
    suspected_handovers = []
    for i in range(0, len(l) - 1, 2):
        
        f1 = os.path.join(dir, l[i])
        f2 = os.path.join(dir, l[i + 1])
        fv1 = os.path.join(dir + "-viz", l[i]) + ".png"
        fv2 = os.path.join(dir + "-viz", l[i + 1]) + ".png"

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
                    # print(f"eccoci qua {hx}{hy}")
                    # print(f"\n\t{x,y}\n")
                    pot = new_map[hx - 1 : hx + 2, hy - 1 : hy + 2]
                    # print(pot)
                    # print(2 in pot)
                    if 2 not in pot:
                        new_t=extract_between_dash_and_json(fv1)
                        print(
                                f"[-] handover detected: {new_t} rel: {(datetime.fromtimestamp(float(new_t))-datetime.fromtimestamp(float(last))).total_seconds()} "
                    
                        )
                        suspected_handovers.append((f1, f2))
            last=extract_between_dash_and_json(fv1)
    return suspected_handovers
