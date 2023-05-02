# this script tries to reach the same target overtime and saves the hops related to starlink
from scapy.all import *
import pyasn
import logging
import csv
from datetime import datetime
import os

def reach_target(target,filename,asndb):
    asndb = pyasn.pyasn(asndb)
    time = datetime.now()
    filename=f"{filename}.csv"
    file_exists=os.path.isfile(filename)
    f=open(filename, "a")
    writer = csv.writer(f)
    if not file_exists:
        writer.writerow(["time", "hop#", "ip"])
    for i in range(4,6):
        myPacket = IP(dst=target, ttl=i) / ICMP()
        res = sr1(myPacket, verbose=0, timeout=3)
        if res:
            src = res.src
            logging.debug(src)
            lookup = asndb.lookup(src)
            if lookup[0] == 14593:
                writer.writerow([time, i, src])
