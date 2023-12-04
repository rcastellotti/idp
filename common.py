"""
this module offers common functions, namely:
"""
import socket
import time
import pyasn
from skyfield.api import Topos, load


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
