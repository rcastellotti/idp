# common stuff used in different scripts
import csv
import logging
import os
from datetime import datetime
import socket

import pyasn
from scapy.all import RandShort, sr, IP, TCP, RandInt, TracerouteResult, conf, ICMP,sr1


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
    for i in range(4, 6):
        pkt = IP(dst=target, ttl=i) / ICMP()
        res = sr1(pkt, verbose=0, timeout=3)
        if res:
            src = res.src
            logging.debug(src)
            lookup = asndb.lookup(src)
            if lookup[0] == 14593:
                writer.writerow([time, i, src])


def traceroute(
        target,
        dport=80,
        minttl=1,
        maxttl=30,
        sport=RandShort(),
        l4=None,
        filter=None,
        timeout=2,
        verbose=None,
        **kargs,
):
    """Instant TCP traceroute traceroute(target, [maxttl=30,] [dport=80,] [sport=80,] [verbose=conf.verb]) -> None"""
    if verbose is None:
        verbose = conf.verb
    if filter is None:
        # we only consider ICMP error packets and TCP packets with at
        # least the ACK flag set *and* either the SYN or the RST flag
        # set
        filter = "(icmp and (icmp[0]=3 or icmp[0]=4 or icmp[0]=5 or icmp[0]=11 or icmp[0]=12)) or (tcp and (tcp[13] & 0x16 > 0x10))"
    if l4 is None:
        a, b = sr(
            IP(dst=target, id=RandShort(), ttl=(minttl, maxttl))
            / TCP(seq=RandInt(), sport=sport, dport=dport),
            timeout=timeout,
            filter=filter,
            verbose=verbose,
            **kargs,
        )
    else:
        # this should always work
        filter = "ip"
        a, b = sr(
            IP(dst=target, id=RandShort(), ttl=(minttl, maxttl)) / l4,
            timeout=timeout,
            filter=filter,
            verbose=verbose,
            **kargs,
        )
    if verbose:
        a = TracerouteResult(a.res)
        a.show()

    hops = []
    if l4 is None:
        for i in a.res:
            t = i[1].getlayer(TCP)
            # we need to check we are not selecting the answers with SYN/AC
            if t is None:
                hops.append(i[1].src)
                continue
    else:
        # only picking intermediate routers
        hops = [i[1].src for i in a if i[1].type == 11]
    return hops



