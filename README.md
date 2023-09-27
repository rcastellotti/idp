# IDP Castellotti

+ `common.py` ~> collection of miscellaneous functions
+ `nine981.py` ~> interact with the gRPC api the dish exposes
+ `cloud-traceroutes.py` ~> the tool to perform (and visualize) traceroutes to cloud datacenters
+ `s.py` ~> cli to use `nine918.py`
+ `map.py` ~> download obstruction maps for a certain amount of seconds (to get meaningful data remember to reboot first)
+ `viz.py` ~> a script to create images to visualize obstruction maps
+ `hand.py` ~> the tool to detect handovers (check `main.ipynb` to see a viz)
+ `visible-satellites.py` ~> extracts visible Starlink satellites (you get to define what "visible" means), sample usage: `python3 visible_satellites.py -v -lat 48.2489 -lon 11.6532 -el 0 -d 800` READY
+ `main.ipynb` ~> scratchpad
+ `big-file.py` ~> a script to measure 
+ `pop-ping-latency.py` ~> can be used to extract pop ping latency from the dish, it is meant to be used while creating some traffic with iperf, to do so: start iperf in server mode on an host with `iper3 -s` 
and send some data with `iperf3 -c <YOUR_IP> -u -b  <YOUR_BW> -t  300`, make sure to set a route for your ip to send traffic trhough the right interface, in our case `ip route add 138.246.253.20 via 192.168.1.1`. 


# IDP Castellotti
## Infra
* The default gateway for starlink is 192.168.1.1
* The API is available at 192.168.100.1
    * A route there is added by the config of the enp1s0f2 interface


`ssh -D 9981 -J <USERNAME>@sshgw.net.in.tum.de root@starlink.net.in.tum.de -p 10022` allows to access the web UI, -D option also allows to use a SOCKS proxy

use `export http_proxy=socks5://localhost:9981` to run commands in a terminal using the proxy 

Can we find which satellite are we connected to?
[This](https://www.reddit.com/r/Starlink/comments/p84o5i/comment/h9o1elp/) pal suggests this might not be possible anymore, the reason I was interested in understanding which satellite we are connected to is to correlate sudden latency spikes and satellite handovers.


* 100.64.0.1 -> carrier grade nat


+ send some constant traffic and then monitor latency (setup a server?)
    + `head -c 512000 /dev/urandom > payload.txt`
    + `while true; do nc -l 1234; done`
    + `while true; do nc localhost 1234 < payload.txt; done`



+ ping two hosts in the same geographic area but in different ASes (in particular one AS peering directly with SpaceX and one not peering directly)


## 18/04 > 02/05
NOTE: we did not meet on 25/04, so i extended this section for 1 week more

+ try to reach the same target with the TTL that causes the GS to reply and monitor if this changes overtime DONE
    + wrote `common.py` (will definitely need a rewrite) 
    + wrote script `reach-single-target.py` and it is now running with `watch -n 30 python3 reach-single-target.py -d /root/idp-castellotti-data/rst `, results are in `idp-castellotti-data/rst`

+ try to reach targets in the same geographic area and see if the GS changes
    + wrote script `same-geo.py` and it is now running with `wathch -n 10 sudo python3 same-geo.py -d /root/idp-castellotti-data/same-geo --asndb /root/idp-castellotti-data/ipasn_20230315.dat `, results are in `idp-castellotti-data/same-geo`
    + seems like reaching the same target uses the same "GS", check (for example)`idp-castellotti-data/same-geo/it/europe-west8-milan-34.0.191.25.csv`, `jp/asia-northeast2-osaka-34.127.177.87.csv`, I guess we can setup a script that monitors a single ip address for each datacenter, `watch -n 60 python3 reach-regions.py -d --starlink /root/idp-castellotti-data/regions --asndb /root/idp-castellotti-data/ipasn_20230315.dat -r cloud-ips.json`


    + i guess we can use the addresses from `cloud-ips.json` to do whatever we need to do.
    + i am afraid maxmind cannot help us locating starlink-related stuff, as every (?) address is located in Ross,Manitoba,Canada, North America https://imgur.com/xeDKVL8.png


Apparently all traffic goes through North America (me1 included), does this happen for "regular connections?" -> run `watch -n 60 python3 reach-regions.py -d /root/idp-castellotti-data/regions-nostarlink --asndb /root/idp-castellotti-data/ipasn_20230315.dat -r cloud-ips.json` removing the line configuring starlink usage


## 02/05 -> 09/05

+ I messed up, doing traceroutes i noticed we are doing one more hop inside as14593, so i changed the ttl parameters in `common.reach_target`, i am pretty sure we were not hitting anything inside as14593 after the 5th hop before, and [these](https://gitlab.lrz.de/netintum/teaching/tumi8-theses/idp-castellotti-data/-/tree/main/traceroutes_cgs) traceroutes seem to confirm my hypothesis, maybe they changed something internally?
+ ran some more traceroutes and saw this (around thursday last week)


### list of geolocated ips 

+ https://www.gstatic.com/ipranges/cloud.json
+ https://ip-ranges.amazonaws.com/ip-ranges.json
+ https://www.microsoft.com/en-us/download/details.aspx?id=53601
+ https://geoip.linode.com/
+ https://digitalocean.com/geo/google.csv
+ https://www.alibabacloud.com/help/en/data-transmission-service/latest/whitelist-dts-ip-ranges-for-your-user-created-database
+ https://cloud.ibm.com/docs/cloud-infrastructure?topic=cloud-infrastructure-ibm-cloud-ip-ranges
+ https://docs.oracle.com/en-us/iaas/tools/public_ip_ranges.json --> incredibily transparent, consider using these 

huge problem with cloud providers -> we lose track of the packet as soon as it enters their network

### sytemd timer related stuff
Let's pick target manually (`targets.csv`)

created systemd timer `traceroute.timer,traceroute.service`

```bash
systemd-analyze verify traceroute.*
cp -r traceroute.* /etc/systemd/system/
systemctl daemon-reload
systemctl start traceroute
systemctl enable traceroute
systemctl status traceroute
journalctl -u traceroute
```


```bash
jupyter notebook --NotebookApp.allow_origin=* --NotebookApp.allow_remote_access=1 --allow-root
```

```bash
ssh -D 9981 -J casr@sshgw.net.in.tum.de root@starlink.net.in.tum.de -p 10022
```
```bash
grpcurl -plaintext -d '{"get_status":{}}' 192.168.100.1:9200 SpaceX.API.Device.Device/Handle | jq ".dishGetStatus.downlinkThroughputBps"

grpcurl -plaintext -d '{"get_status":{}}' 192.168.100.1:9200 SpaceX.API.Device.Device/Handle | jq ".dishGetStatus.popPingLatencyMs"
```

We need to understand better what it is happening inside the network, what we see now is just a mess.

+ extend traceroutes to have rtts ✅
+ run `iperf3` to create some constant background noise to a target J. will setup
    + server: `iperf -s -u`
    + client: `iperf -c 138.246.253.20 -p 5001 -u -b 5k` 
+ running for some time: `sudo python3 traceroutes_stress.py` (saving results in `~/idp-castellotti/data/traceroutes-iperf-5bks`) (typo)


additional: 
+ extract the latency for THAT certain period of time from the dish
+ compare latency measurements from the dish

# 23-05 -> 30/05

+ add a route for 138.246.253.20
    + ip route add 138.246.253.20 via 192.168.1.1
    + 
+ ping the first host after starlink while iperfing some data (incrementally) to see whether we see changes in latency, will use `213.144.184.30`

```
% ping 213.144.184.30 -c 10                                                                   27 2 pts/1 ~ rc@gnolmir 23-05-23 17:34:29
PING 213.144.184.30 (213.144.184.30) 56(84) bytes of data.
64 bytes from 213.144.184.30: icmp_seq=1 ttl=57 time=11.3 ms
64 bytes from 213.144.184.30: icmp_seq=2 ttl=57 time=10.9 ms
64 bytes from 213.144.184.30: icmp_seq=3 ttl=57 time=12.7 ms
64 bytes from 213.144.184.30: icmp_seq=4 ttl=57 time=11.1 ms
64 bytes from 213.144.184.30: icmp_seq=5 ttl=57 time=10.6 ms
64 bytes from 213.144.184.30: icmp_seq=6 ttl=57 time=10.5 ms
64 bytes from 213.144.184.30: icmp_seq=7 ttl=57 time=10.5 ms
64 bytes from 213.144.184.30: icmp_seq=8 ttl=57 time=11.6 ms
64 bytes from 213.144.184.30: icmp_seq=9 ttl=57 time=12.8 ms
64 bytes from 213.144.184.30: icmp_seq=10 ttl=57 time=10.3 ms

--- 213.144.184.30 ping statistics ---
10 packets transmitted, 10 received, 0% packet loss, time 9014ms
rtt min/avg/max/mdev = 10.264/11.227/12.771/0.841 ms
```

## iperf3 -c 138.246.253.20 -u -b 10K -t 3600

```
% ping 213.144.184.30 -c 10                                                                   26 2 pts/1 ~ rc@gnolmir 23-05-23 17:34:15
PING 213.144.184.30 (213.144.184.30) 56(84) bytes of data.
64 bytes from 213.144.184.30: icmp_seq=1 ttl=57 time=12.2 ms
64 bytes from 213.144.184.30: icmp_seq=2 ttl=57 time=10.8 ms
64 bytes from 213.144.184.30: icmp_seq=3 ttl=57 time=10.7 ms
64 bytes from 213.144.184.30: icmp_seq=4 ttl=57 time=12.7 ms
64 bytes from 213.144.184.30: icmp_seq=5 ttl=57 time=21.3 ms
64 bytes from 213.144.184.30: icmp_seq=6 ttl=57 time=11.4 ms
64 bytes from 213.144.184.30: icmp_seq=7 ttl=57 time=13.3 ms
64 bytes from 213.144.184.30: icmp_seq=8 ttl=57 time=12.9 ms
64 bytes from 213.144.184.30: icmp_seq=9 ttl=57 time=17.1 ms
64 bytes from 213.144.184.30: icmp_seq=10 ttl=57 time=11.2 ms

--- 213.144.184.30 ping statistics ---
10 packets transmitted, 10 received, 0% packet loss, time 9014ms
rtt min/avg/max/mdev = 10.709/13.365/21.308/3.184 ms
```

## iperf3 -c 138.246.253.20 -u -b 20K -t 3600

```
% ping 213.144.184.30 -c 10                                                                   27 2 pts/1 ~ rc@gnolmir 23-05-23 17:34:54
PING 213.144.184.30 (213.144.184.30) 56(84) bytes of data.
64 bytes from 213.144.184.30: icmp_seq=1 ttl=57 time=12.7 ms
64 bytes from 213.144.184.30: icmp_seq=2 ttl=57 time=12.9 ms
64 bytes from 213.144.184.30: icmp_seq=3 ttl=57 time=17.2 ms
64 bytes from 213.144.184.30: icmp_seq=4 ttl=57 time=13.1 ms
64 bytes from 213.144.184.30: icmp_seq=5 ttl=57 time=10.5 ms
64 bytes from 213.144.184.30: icmp_seq=6 ttl=57 time=15.3 ms
64 bytes from 213.144.184.30: icmp_seq=7 ttl=57 time=14.1 ms
64 bytes from 213.144.184.30: icmp_seq=8 ttl=57 time=11.9 ms
64 bytes from 213.144.184.30: icmp_seq=9 ttl=57 time=11.7 ms
64 bytes from 213.144.184.30: icmp_seq=10 ttl=57 time=19.0 ms

--- 213.144.184.30 ping statistics ---
10 packets transmitted, 10 received, 0% packet loss, time 9014ms
rtt min/avg/max/mdev = 10.476/13.831/18.997/2.501 ms
```
## iperf3 -c 138.246.253.20 -u -b 50K -t 3600

```
% ping 213.144.184.30 -c 10                                                                   27 2 pts/1 ~ rc@gnolmir 23-05-23 17:35:32
PING 213.144.184.30 (213.144.184.30) 56(84) bytes of data.
64 bytes from 213.144.184.30: icmp_seq=1 ttl=57 time=10.7 ms
64 bytes from 213.144.184.30: icmp_seq=2 ttl=57 time=10.8 ms
64 bytes from 213.144.184.30: icmp_seq=3 ttl=57 time=11.3 ms
64 bytes from 213.144.184.30: icmp_seq=4 ttl=57 time=16.1 ms
64 bytes from 213.144.184.30: icmp_seq=5 ttl=57 time=11.3 ms
64 bytes from 213.144.184.30: icmp_seq=6 ttl=57 time=10.2 ms
64 bytes from 213.144.184.30: icmp_seq=7 ttl=57 time=13.3 ms
64 bytes from 213.144.184.30: icmp_seq=8 ttl=57 time=10.7 ms
64 bytes from 213.144.184.30: icmp_seq=9 ttl=57 time=18.2 ms
64 bytes from 213.144.184.30: icmp_seq=10 ttl=57 time=10.2 ms

--- 213.144.184.30 ping statistics ---
10 packets transmitted, 10 received, 0% packet loss, time 9013ms
rtt min/avg/max/mdev = 10.187/12.289/18.239/2.618 ms
```
## iperf3 -c 138.246.253.20 -u -b 100k -t 3600

```
% ping 213.144.184.30 -c 10                                                                   29 2 pts/1 ~ rc@gnolmir 23-05-23 17:36:50
PING 213.144.184.30 (213.144.184.30) 56(84) bytes of data.
64 bytes from 213.144.184.30: icmp_seq=1 ttl=57 time=14.3 ms
64 bytes from 213.144.184.30: icmp_seq=2 ttl=57 time=11.3 ms
64 bytes from 213.144.184.30: icmp_seq=3 ttl=57 time=17.8 ms
64 bytes from 213.144.184.30: icmp_seq=4 ttl=57 time=10.8 ms
64 bytes from 213.144.184.30: icmp_seq=5 ttl=57 time=17.0 ms
64 bytes from 213.144.184.30: icmp_seq=6 ttl=57 time=10.9 ms
64 bytes from 213.144.184.30: icmp_seq=7 ttl=57 time=10.9 ms
64 bytes from 213.144.184.30: icmp_seq=8 ttl=57 time=10.2 ms
64 bytes from 213.144.184.30: icmp_seq=9 ttl=57 time=13.2 ms
64 bytes from 213.144.184.30: icmp_seq=10 ttl=57 time=10.7 ms

--- 213.144.184.30 ping statistics ---
10 packets transmitted, 10 received, 0% packet loss, time 9013ms
rtt min/avg/max/mdev = 10.237/12.715/17.783/2.618 ms
```

## iperf3 -c 138.246.253.20 -u -b 1M -t 3600
```
130 % ping 213.144.184.30 -c 10                                                               29 2 pts/1 ~ rc@gnolmir 23-05-23 17:38:08
PING 213.144.184.30 (213.144.184.30) 56(84) bytes of data.
64 bytes from 213.144.184.30: icmp_seq=1 ttl=57 time=11.2 ms
64 bytes from 213.144.184.30: icmp_seq=2 ttl=57 time=13.4 ms
64 bytes from 213.144.184.30: icmp_seq=3 ttl=57 time=10.6 ms
64 bytes from 213.144.184.30: icmp_seq=4 ttl=57 time=10.0 ms
64 bytes from 213.144.184.30: icmp_seq=5 ttl=57 time=10.3 ms
64 bytes from 213.144.184.30: icmp_seq=6 ttl=57 time=11.1 ms
64 bytes from 213.144.184.30: icmp_seq=7 ttl=57 time=10.1 ms
64 bytes from 213.144.184.30: icmp_seq=8 ttl=57 time=18.0 ms
64 bytes from 213.144.184.30: icmp_seq=9 ttl=57 time=10.6 ms
64 bytes from 213.144.184.30: icmp_seq=10 ttl=57 time=12.2 ms

--- 213.144.184.30 ping statistics ---
10 packets transmitted, 10 received, 0% packet loss, time 9011ms
rtt min/avg/max/mdev = 10.012/11.758/18.019/2.305 ms
```

## iperf3 -c 138.246.253.20 -u -b 10M -t 3600
```
% ping 213.144.184.30 -c 10                                                                   29 2 pts/1 ~ rc@gnolmir 23-05-23 17:38:42
PING 213.144.184.30 (213.144.184.30) 56(84) bytes of data.
64 bytes from 213.144.184.30: icmp_seq=1 ttl=57 time=12.2 ms
64 bytes from 213.144.184.30: icmp_seq=2 ttl=57 time=10.2 ms
64 bytes from 213.144.184.30: icmp_seq=3 ttl=57 time=16.0 ms
64 bytes from 213.144.184.30: icmp_seq=4 ttl=57 time=10.8 ms
64 bytes from 213.144.184.30: icmp_seq=5 ttl=57 time=11.3 ms
64 bytes from 213.144.184.30: icmp_seq=6 ttl=57 time=12.2 ms
64 bytes from 213.144.184.30: icmp_seq=7 ttl=57 time=14.4 ms
64 bytes from 213.144.184.30: icmp_seq=8 ttl=57 time=10.3 ms
64 bytes from 213.144.184.30: icmp_seq=9 ttl=57 time=11.0 ms
64 bytes from 213.144.184.30: icmp_seq=10 ttl=57 time=11.2 ms

--- 213.144.184.30 ping statistics ---
10 packets transmitted, 10 received, 0% packet loss, time 9011ms
rtt min/avg/max/mdev = 10.187/11.961/16.004/1.777 ms
```
## iperf3 -c 138.246.253.20 -u -b 100M -t 3600
```
% ping 213.144.184.30 -c 10                                                                   29 2 pts/1 ~ rc@gnolmir 23-05-23 17:38:52
PING 213.144.184.30 (213.144.184.30) 56(84) bytes of data.
64 bytes from 213.144.184.30: icmp_seq=1 ttl=57 time=10.1 ms
64 bytes from 213.144.184.30: icmp_seq=2 ttl=57 time=12.5 ms
64 bytes from 213.144.184.30: icmp_seq=3 ttl=57 time=10.6 ms
64 bytes from 213.144.184.30: icmp_seq=4 ttl=57 time=10.7 ms
64 bytes from 213.144.184.30: icmp_seq=5 ttl=57 time=10.7 ms
64 bytes from 213.144.184.30: icmp_seq=6 ttl=57 time=14.2 ms
64 bytes from 213.144.184.30: icmp_seq=7 ttl=57 time=10.1 ms
64 bytes from 213.144.184.30: icmp_seq=8 ttl=57 time=13.4 ms
64 bytes from 213.144.184.30: icmp_seq=9 ttl=57 time=11.0 ms
64 bytes from 213.144.184.30: icmp_seq=10 ttl=57 time=18.0 ms

--- 213.144.184.30 ping statistics ---
10 packets transmitted, 10 received, 0% packet loss, time 9013ms
rtt min/avg/max/mdev = 10.069/12.123/18.030/2.391 ms
```



now running 

```
iperf3 -c 138.246.253.20 -u -b 10K -t 3600 
bash ping.sh 213.144.184.30 > iperf-10k.csv

iperf3 -c 138.246.253.20 -u -b 20K -t 3600 
bash ping.sh 213.144.184.30 > iperf-20k.csv

iperf3 -c 138.246.253.20 -u -b 50K -t 3600 
bash ping.sh 213.144.184.30 > iperf-50k.csv

iperf3 -c 138.246.253.20 -u -b 100K -t 3600 
bash ping.sh 213.144.184.30 > iperf-100k.csv

iperf3 -c 138.246.253.20 -u -b 1M -t 3600 
bash ping.sh 213.144.184.30 > iperf-1M.csv

iperf3 -c 138.246.253.20 -u -b 10M -t 3600 
bash ping.sh 213.144.184.30 > iperf-10M.csv
```

Created a box plot to visualize what happens



1) measure latency with ping
2) extract latency from the dish
3) run iperf

## 30/05 -->
+ start filtering "visible satellites" by distance, prolly ~800km
+ download a big chonky file (` wget -4 https://speed.hetzner.de/10GB.bin --report-speed=bits -O /dev/null --bind-address 192.168.1.196`) 


check how much the satellite numbers dec increasing the distance 

restoring route sudo ip route add 192.168.100.1 via 192.168.1.1



http://geoip.starlinkisp.net/feed.csv
https://gist.github.com/rcastellotti/e20630366dfeaeada6cc2680f562f6ac



mention the bandwidth the dish reports is true
mettere in appendix blocchi di codice