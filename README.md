## todo
+ script `common.py` has some optimization (only using ttls from 4 to 6). maybe we should change this when producing
final results to be sure we are indeed checking all the hops


## sample usage for `common.traceroute`

```python
import socket
from common import traceroute
from scapy.all import *

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
```