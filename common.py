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
from pathlib import Path


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
            results.append([probe_timestamp,ttl,"*","*","*","*"])
            ttl+=1
        else:
            hostname = ""
            try:
                hostname = socket.gethostbyaddr(reply.src)[0]
            except socket.herror:
                hostname = "???"
            asn = asndb.lookup(reply.src)[0]
            rtt_ms=(reply.time - pkt.sent_time)*1000

            r = (probe_timestamp, ttl, reply.src, hostname, asn,rtt_ms)
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



def run_traceroute_and_save_to_file(filename,ip,protocol,asndb):
    logging.debug(f"traceroute: {filename}")
    file_exists = os.path.isfile(filename)
    with open(filename, "a") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(("timestamp", "hop", "ip", "hostname", "asn","rtt"))
        results = traceroute(ip, protocol, asndb=asndb)
        writer.writerows(results)


def cloud_traceroutes(region_file,output_directory,asndb):
    with open(region_file, "r") as csvfile:
        next(csvfile)  # skipping the header
        reader = csv.reader(csvfile)

        for row in reader:
            provider, region, ip = row
            dir = output_directory
            Path(dir+"/"+provider).mkdir(parents=True, exist_ok=True)

            # for protocol in ["ICMP", "UDP", "TCP"]:   
            for protocol in ["ICMP"]:         
                dt=datetime.datetime.now().isoformat()
                # normal
                filename = f"{dir}/{provider}/{region}-{ip}-{dt}-{protocol}-normal.csv"
                run_traceroute_and_save_to_file(filename,ip,protocol,asndb)
                # starlink
                conf.route.add(net="0.0.0.0/0", gw="192.168.1.1")
                filename = f"{dir}/{provider}/{region}-{ip}-{dt}-{protocol}-starlink.csv"
                run_traceroute_and_save_to_file(filename,ip,protocol,asndb)
                conf.route.delt(net="0.0.0.0/0", gw="192.168.1.1")
