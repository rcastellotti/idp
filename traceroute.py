from scapy.all import RandShort, sr, IP, TCP, UDP, RandInt, TracerouteResult, conf, ICMP
import socket

# # conf.route.add(net="0.0.0.0/0", gw="192.168.1.1")


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


hostname = "garr.it"

hops = traceroute(hostname, verbose=0)
for i, hop in enumerate(hops):
    print(f"{i} = {hop} -> {socket.getnameinfo((hop, 0), 0)[0]}")

hops = traceroute(hostname, l4=UDP(sport=RandShort(), dport=53), verbose=0)
for i, hop in enumerate(hops):
    print(f"{i} = {hop} -> {socket.getnameinfo((hop, 0), 0)[0]}")

hops = traceroute(hostname, l4=ICMP(), verbose=0)
for i, hop in enumerate(hops):
    print(f"{i} = {hop} -> {socket.getnameinfo((hop, 0), 0)[0]}")
