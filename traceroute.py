from scapy.all import sr1, IP, conf, ICMP
import socket
import logging

# conf.route.add(net="0.0.0.0/0", gw="192.168.1.1")


def traceroute():
    hops = []
    for i in range(32):
        p = sr1(IP(dst="tum.de", ttl=i) / ICMP(), verbose=0, timeout=1)
        if p is None:
            hops.append("*")
            print(f"{i} -> *")
            continue
        logging.debug(p)
        hops.append(p.src)
        print(f"{i} -> {p.src} --> {socket.getnameinfo((p.src, 0), 0)[0]}")
        if p.type == 0:
            break
    return hops


hops = traceroute()
print(hops)
