# common stuff used in different scripts
import csv
import logging
import os
from datetime import datetime
import socket
import time
import pyasn
from scapy.all import RandShort, sr, IP, TCP, RandInt, TracerouteResult, conf, ICMP, sr1, UDP
import datetime

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


def traceroute(target, protocol, asndb):
    asndb = pyasn.pyasn(asndb)

    ttl = 1
    probe_timestamp = int(time.time())
    results = []
    while ttl <30 :
        pkt_base = IP(dst=target, ttl=ttl)

        if protocol == "ICMP":
            pkt = pkt_base / ICMP()
        elif protocol == "UDP":
            pkt = pkt_base / UDP(dport=53)
        elif protocol == "TCP":
            pkt = pkt_base / TCP(dport=80, flags="S")
        
        reply = sr1(pkt, verbose=False, timeout=1)
        
        if reply is None:
            results.append([probe_timestamp,ttl,"*","*","*"])
            ttl+=1
        else:
            hostname = ""
            try:
                hostname = socket.gethostbyaddr(reply.src)[0]
            except socket.herror:
                hostname = "???"
            asn = asndb.lookup(reply.src)[0]
            r = (probe_timestamp, ttl, reply.src, hostname, asn)
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

