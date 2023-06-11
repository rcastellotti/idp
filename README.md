# IDP Castellotti

## sample usage for `common.traceroute`
!! make sure to configure the correct interface!!

```python
import socket
from common import traceroute
from scapy.all import *
# conf.route.add(net="0.0.0.0/0", gw="192.168.1.1") # interface config in our case
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


## `main.ipynb`

A simple notebook to test stuff implemented in other files


## `pop_ping_latency.py`
This script can be used to extract pop ping latency from the dish, it is meant to be used while creating some traffic with iperf, to do so: start iperf in server mode on an host with `iper3 -s` 
and send some data with `iperf3 -c <YOUR_IP> -u -b  <YOUR_BW> -t  300`, make sure to set a route for your ip to send traffic trhough the right interface, in our case `ip route add 138.246.253.20 via 192.168.1.1`. Additionally here is a script I used to run iperf with different bandwidths:
```bash
#!/bin/bash
set -xe

bandwidths=("10k" "20k" "50k" "100k" "1M" "10M")
server_ip="138.246.253.20"
duration=300

for bandwidth in "${bandwidths[@]}"; do
  iperf3 -c "$server_ip" -u -b "$bandwidth" -t "$duration"
done
```

## `starlink_grpc.py`
This is adapted from <https://github.com/sparky8512/starlink-grpc-tools/blob/main/starlink_grpc.py>, because I needed just a subset of that, in case you need more use [`starlink-grpc-tools`](https://github.com/sparky8512/starlink-grpc-tools)

## `visible-satellites.py`

Get all visible satellites, where "visible" is defined as above the horizon and within the distance passed as parameter, following are garching's coordinates

```bash
python3 visible_satellites.py \
    -lat 48.2489 \
    -lon 11.6532 \
    -el 0 \
    -d 800 \
    -o /home/rc/idp-castellotti-data/visible_satellites_garching.csv
```