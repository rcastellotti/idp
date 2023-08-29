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



Additionally here is a script I used to run iperf with different bandwidths:
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



in the report: list all the external tools we are using

--------------------

keep this to explain how we are detecting handovers

  # import json
# import numpy as np
# f1 = "map-bw-stuff2/1691158076.json"
# f2 = "map-bw-stuff2/1691158077.json"
# map1 = json.load(open(f1))
# map1 = map1["dishGetObstructionMap"]["snr"]
# map1 = np.array(map1).reshape(123, 123)
# map2 = json.load(open(f2))
# map2 = map2["dishGetObstructionMap"]["snr"]
# map2 = np.array(map2).reshape(123, 123)

# # visualize_handover(f1,f2)
# new=map1+map2
# rows, cols = np.where(new == 0)
# zero_coordinates = list(zip(rows, cols))

# for coord in zero_coordinates:
#     hx=coord[0]
#     hy=coord[1]
#     pot = new[hx - 1 : hx + 2, hy - 1 : hy + 2]
#     print(pot)
#     if not 2 in pot:
#         print("detected handover")

# plt.figure()
# plt.imshow(new)



----------------





# # https://web.archive.org/web/20220320174537/https://ecfsapi.fcc.gov/file/1020316268311/Starlink%20Services%20LLC%20Application%20for%20ETC%20Designation.pdf


https://en.wikipedia.org/wiki/Two-line_element_set
https://rhodesmill.org/skyfield/
https://www.space-track.org/documentation#/tle






``---
tags: student
---


# IDP Castellotti
## Infra
* The default gateway for starlink is 192.168.1.1
* The API is available at 192.168.100.1
    * A route there is added by the config of the enp1s0f2 interface
* The regular uplink is on porta enp3s0
* Starlink is attached to enp1s0f2
* A 60GHz link is attached to enp1s0f3, don't worry about this one
    * Just don't change that interfaces config
* A user `test` currently exists, in whose home some tooling resides
    * Feel free to add a new user for working on the machine

## 2023-03-08
* We will provide remote access to the dish
    * No static IP yet
* Tools you can look at for now:
    * https://github.com/danopstech/starlink_exporter
    * https://github.com/sparky8512/starlink-grpc-tools


## Misc

`ssh -D 9981 -J <USERNAME>@sshgw.net.in.tum.de root@starlink.net.in.tum.de -p 10022` allows to access the web UI, -D option also allows to use a SOCKS proxy

use `export http_proxy=socks5://localhost:9981` to run commands in a terminal using the proxy 

Can we find which satellite are we connected to?
[This](https://www.reddit.com/r/Starlink/comments/p84o5i/comment/h9o1elp/) pal suggests this might not be possible anymore, the reason I was interested in understanding which satellite we are connected to is to correlate sudden latency spikes and satellite handovers.

Every satellite has a NORAD number, using this number we can retrieve the position of a starlink satellite using this api: https://www.n2yo.com/api/#positions, maybe it is simpler to just check for the position of satellites "above" Garching and see if the moment a satellite gets "too far" is the same moment we have an increase in latency.
What is the metric? Point to point distance?

Here is an API key for an account I created (with a fictitious username): `Z8QNAU-UH9ZP6-28P9MU-507X`
token for ipinfo.io (random username) `18e09b19d7ee9e`

This is the satellite position:

```javascript=
{
  "satlatitude": -39.90318514,
  "satlongitude": 158.28897924,
  "sataltitude": 417.85,
  "azimuth": 254.31,
  "elevation": -69.09,
  "ra": 44.77078138,
  "dec": -43.99279118,
  "timestamp": 1521354418
}
```

I think this could be a good approximation of a point to point distance, used values come from the example api call

```python=
from geopy.distance import distance
from geopy.point import Point
from math import sqrt,pow

altitude=417.85
satlat=-39.90318514
satlong=158.28897924

groundlat=41.702
groundlong=-76.014

a = Point(groundlat,groundlong, 0)
b = Point(satlat,satlong , 0)
ground_distance=distance(a, b)
real_distance=sqrt(pow(alt,2)+pow(ground_distance.km,2))

print(f"ground_distance:{ground_distance}")
print(f"real_distance:{real_distance}")
```

This might be completely wrong, here is the documentation for the distance function  [geopy.distance](https://geopy.readthedocs.io/en/stable/#module-geopy.distance)

Can we understand something more about the hops a packet goes through?

* Todos
    * Test traceroutes over several days
    * Test different targets and protocols
    * map targets to ASes -> https://github.com/hadiasghari/pyasn
        * https://bgp.he.net/
        * Try to see what is the last IP operated by the starlink AS
        * 100.64.0.1 -> carrier grade nat
    * Analyze the latency of the dish -> there is an api endpoint for that
        * Are there specific jumps that might be satelite changes
    * How fast is air: speed of light



## 03-16 -> 03-23

+ now running traceroutes using the `run_traceroutes.sh` script

tricky way for now: `watch -n0.5 python3 dish_grpc_sqlite.py sqlite.db ping_latency`, reading the data in the python notebook  
```sql=
sqlite> .schema ping_stats --indent
CREATE TABLE IF NOT EXISTS "ping_stats"(
  "time" INTEGER NOT NULL,
  "id" TEXT NOT NULL,
  "samples" INTEGER,
  "end_counter" INTEGER,
  "total_ping_drop" REAL,
  "count_full_ping_drop" INTEGER,
  "count_obstructed" INTEGER,
  "total_obstructed_ping_drop" REAL,
  "count_full_obstructed_ping_drop" INTEGER,
  "count_unscheduled" INTEGER,
  "total_unscheduled_ping_drop" REAL,
  "count_full_unscheduled_ping_drop" INTEGER,
  "init_run_fragment" INTEGER,
  "final_run_fragment" INTEGER,
  "run_seconds" INTEGER,
  "run_minutes" INTEGER,
  "mean_all_ping_latency" REAL,
  "deciles_all_ping_latency" REAL,
  "mean_full_ping_latency" REAL,
  "deciles_full_ping_latency" REAL,
  "stdev_full_ping_latency" REAL,
  "load_bucket_samples" INTEGER,
  "load_bucket_min_latency" REAL,
  "load_bucket_median_latency" REAL,
  "load_bucket_max_latency" REAL,
  PRIMARY KEY("time","id")
);
```

## run a python notebook
```bash=
jupyter notebook --NotebookApp.allow_origin=* --NotebookApp.allow_remote_access=1 --allow-root
```

## run simple server to download files
```bash=
python3 -m http.server http://0.0.0.0:8000/ 
```


## asns

+ 137 -> Consortium GARR
+ 195 -> San Diego Supercomputing Center
+ 680 ->  Verein zur Foerderung eines Deutschen Forschungsnetzes e.V.
+ 1299 -> Arelion Sweden AB (twelve99.net)
+ 1741 -> AS1741 CSC - Tieteen tietotekniikan keskus Oy
+ 1909 -> San Diego Supercomputing Center
+ 2152 -> California State University, Office of the Chancellor
+ 2603 -> NORDUNet
+ 3356 -> Level 3 Parent, LLC
+ 6453 -> TATA COMMUNICATIONS (AMERICA) INC
+ 6762 -> TELECOM ITALIA SPARKLE S.p.A.
+ 12816 -> Leibniz-Rechenzentrum
+ 14593 -> Space Exploration Technologies Corporation
+ 16625 -> Akamai Technologies, Inc.
+ 20940 -> Akamai International B.V. (netherlands)
+ 34984 -> Superonline Iletisim Hizmetleri A.S. (turkey)
+ 201011 -> Core-Backbone GmbH


Seems like SpaceX only owns AS14593, announces <https://bgp.he.net/AS14593#_prefixes>
but it seems we are only reaching 206.224.65.0/24 ips


    
`check_ground_station.sh` is a simple script to perform some traceroutes, we are using them to find the first hop after the starlink network, this should be indicative of the exit point.

`gsc.py -H caida.org -P icmp` shows first hop after starlink network, ground station seems to stay the same

now running:

```
*/30 * * * * /usr/bin/bash /root/idp-castellotti/gsc.sh
````

# new stuff
+ direct peerings with as15593: <https://bgp.he.net/AS14593#_peers>

+ `locate_satellite.ipynb` ([skyfield](https://rhodesmill.org/skyfield/earth-satellites.html)) with data directly from [celestrak](https://celestrak.org/NORAD/elements/gp.php?GROUP=starlink&FORMAT=tle)

+ send some constant traffic and then monitor latency (setup a server?)
    + `head -c 512000 /dev/urandom > payload.txt`
    + `while true; do nc -l 1234; done`
    + `while true; do nc localhost 1234 < payload.txt; done`


## 12/04-19/04

We see different ground stations for different hosts, now let's try to:
+ ping two hosts in the same geographic area but in different ASes (in particular one AS peering directly with SpaceX and one not peering directly)

+ does it make any sense to measure whether the latency is lower in this case?

traffic directed to South Africa could exit in Frankfurt bc it could be cheaper (direct peering)



+ get list of ASes directly peering
+ get prefixes for all ASes
+ executee a rDNS query
+ obtain the host to traceroute inside that AS



### what I did

+ wrote `ip-peering-ases.py`, usage:

```bash
python3 ip-peering-ases.py \
    --ases 50 --prefix 5 \
    -i ../idp-castellotti-data/20230401.as-rel.txt \
    -o ../idp-castellotti-data/ip-peering-ases.csv
```

+ creates a file containg the info we want
+ uses stat.ripe.net to get prefixes announced by an AS and AS name
+ uses data from [caida.org/datasets/as-relationships](https://publicdata.caida.org/datasets/as-relationships/serial-1/20230401.as-rel.txt.bz2




)
+ removed every line not containing 14593 using `:v/14593/d` in vim (hacky, btw I use vim) , comparing with https://bgp.he.net/AS14593#_peers (both ipv4 and 6) we have something not present, such as `263237`

cat ip-peering-ases.csv | column -t -s, | less -S



| ASes we are peered with                         | host we can reach in same geo but different AS  |
| ----------------------------------------------- | ----------------------------------------------  |
| 20811 > BRENNERCOM-AS - Brennercom S.p.A.       | uniroma1.it > AS137 > Consortium GARR           |
|  8426 > CLARANET-AS - Claranet Limited          | machester.ac.uk >  AS786 > Jisc Services Limited|
| 20932 > SIG-ST - Services Industriels de Geneve | unige.ch > AS559 > SWITCH                       |
| 1798  > OREGON                                  | oregon.gov > AS394572 > Tyler Technologies, Inc |

does not work:

+ enel.it > AS19551 > Incapsula Inc
+ governo.it > AS20940 > Akamai International B.V. 
+ gov.uk > AS54113 > Fastly, Inc.
+ uoregon.edu > AS54113 > Fastly, Inc.
+ www.unimelb.edu.au >  AS13335 > Cloudflare, Inc. (found while searching something to compare with AS 7575 AARNET-AS-AP Australian Academic and Research Network AARNet)


I ran bash script.sh > report.txt

```
AS 1798 OREGON (192.149.16.194)  and oregon.gov

===ICMP===
tr 192.149.16.194 ===> 206.224.65.202 > 206.224.65.188
tr oregon.gov ===> 206.224.65.206 > 206.224.65.184

===UDP===
tr 192.149.16.194 ===> 206.224.65.198 > 206.224.65.188
tr oregon.gov ===> 206.224.65.198 > 206.224.65.180

===TCP===
no info

AS 20932 SIG-ST - Services Industriels de Geneve (185.68.206.75) and unige.ch

===ICMP===
tr 185.68.206.75 ===> 206.224.65.206 > 206.224.65.192
tr unige.ch ===> 206.224.65.198 > 206.224.65.190

===UDP===
tr 185.68.206.75 ===> 206.224.65.194 > 206.224.65.190
tr unige.ch ===> 206.224.65.206 > 206.224.65.188

===TCP===
tr 185.68.206.75 ===> 206.224.65.190
tr 185.68.206.75 ===> 206.224.65.184


AS 8426  CLARANET-AS - Claranet Limited	(194.15.233.244) and manchester.ac.uk

===ICMP===
tr 194.15.233.244 ===> 206.224.65.198 > 206.224.65.182
tr manchester.ac.uk ===> 206.224.65.194 > 206.224.65.186

===UDP===
tr 194.15.233.244 ===> 206.224.65.194 > 206.224.65.180
tr machester.ac.uk ===> 206.224.65.202 > 206.224.65.180

===TCP===
tr 194.15.233.244 ===> 206.224.65.192
tr machester.ac.uk ===> 206.224.65.188

AS 20811 > BRENNERCOM-AS - Brennercom S.p.A. (95.171.35.164) and uniroma1.it

===ICMP===
tr 95.171.35.164 ===> 206.224.65.198 > 206.224.65.190
tr uniroma1.it ===> 206.224.65.202 > 206.224.65.180

===UDP===
tr 95.171.35.164 ===> 206.224.65.198 > 206.224.65.182
tr uniroma1.it ===> 206.224.65.202 > 206.224.65.186

===TCP===
tr 95.171.35.164 ===> no info
tr uniroma1.it ===> 206.224.65.178
```

This can be easily scripted (pyasn), I am not sure this proves anything.


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

### some additional stuff, visualize all the routers inside starlink as14593
```
root@gnolmir ~/i/regions (main)# cut -d, -f3 *.csv | sort | uniq -c | sort -rn
    595 206.224.65.204
    595 206.224.65.200
    549 206.224.65.208
    444 206.224.65.182
    440 206.224.65.196
    360 206.224.65.188
    358 206.224.65.129
    274 206.224.65.178
    235 206.224.65.180
    189 206.224.65.184
    159 206.224.65.186
    151 206.224.65.190
     40 ip
```

Apparently all traffic goes through North America (me1 included), does this happen for "regular connections?" -> run `watch -n 60 python3 reach-regions.py -d /root/idp-castellotti-data/regions-nostarlink --asndb /root/idp-castellotti-data/ipasn_20230315.dat -r cloud-ips.json` removing the line configuring starlink usage


## 02/05 -> 09/05

+ I messed up, doing traceroutes i noticed we are doing one more hop inside as14593, so i changed the ttl parameters in `common.reach_target`, i am pretty sure we were not hitting anything inside as14593 after the 5th hop before, and [these](https://gitlab.lrz.de/netintum/teaching/tumi8-theses/idp-castellotti-data/-/tree/main/traceroutes_cgs) traceroutes seem to confirm my hypothesis, maybe they changed something internally?
+ ran some more traceroutes and saw this (around thursday last week)

```bash
(venv) root@gnolmir ~/i/regions (main)# cut -d, -f3 *.csv | sort | uniq -c | sort -rn
    683 206.224.65.200
    682 206.224.65.204
    629 206.224.65.208
    508 206.224.65.182
    504 206.224.65.196
    416 206.224.65.188
    414 206.224.65.192
    314 206.224.65.178
    267 206.224.65.180
    213 206.224.65.184
    183 206.224.65.186
    175 206.224.65.190
    128 149.19.109.49
    120 149.19.109.47
     40 ip
```

```text
traceroute to 149.19.109.47 (149.19.109.47), 30 hops max, 60 byte packets
 1  ac.scylla.net.in.tum.de (131.159.14.129)  1.241 ms  1.218 ms  1.229 ms
 2  nz-bb1-net.in.tum.de (131.159.252.147)  2.057 ms  2.045 ms  2.106 ms
 3  nz-csr1-kw5-bb1.rbg.tum.de (131.159.252.2)  2.719 ms  2.972 ms  3.266 ms
 4  vl-3010.csr1-2wr.lrz.de (129.187.0.149)  2.810 ms  3.206 ms  3.684 ms
 5  cr-gar1-be2-147.x-win.dfn.de (188.1.37.89)  3.091 ms  3.332 ms  3.352 ms
 6  cr-erl2-be5.x-win.dfn.de (188.1.144.213)  7.089 ms  5.138 ms  5.249 ms
 7  * * *
 8  * * *
 9  * * *
10  * * *
11  * * *
12  * * *
13  100ge0-36.core1.pdx3.he.net (184.104.195.46)  150.112 ms * *
14  100ge0-36.core1.pdx2.he.net (184.104.195.66)  150.765 ms  151.005 ms 100ge0-35.core1.akl2.he.net (184.104.195.146)  279.094 ms
15  100ge0-54.core1.akl1.he.net (184.104.196.118)  277.287 ms 100ge0-36.core1.pdx3.he.net (184.104.195.46)  150.462 ms 100ge0-54.core1.akl1.he.net (184.104.196.118)  277.590 ms
16  space-exploration-technologies-corp.e0-7.core1.akl1.he.net (72.52.83.198)  275.603 ms 100ge0-35.core1.akl2.he.net (184.104.195.146)  278.671 ms  279.321 ms
17  * 100ge0-54.core1.akl1.he.net (184.104.196.118)  278.217 ms  277.882 ms
18  * * space-exploration-technologies-corp.e0-7.core1.akl1.he.net (72.52.83.198)  275.445 ms
19  * * *
20  * * *
21  * * *
22  * * *
23  * * *
24  * * *
25  * * *
26  * * *
27  * * *
28  * * *
29  * * *
30  * * *
```

We see some spacex stuff, now (Tuesday) I cannot see that hop anymore, am I getting crazy?

09/05 13:00
```
root@gnolmir ~/i/regions (main)# traceroute -i enp1s0f2 34.81.202.211
traceroute to 34.81.202.211 (34.81.202.211), 30 hops max, 60 byte packets
 1  192.168.1.1 (192.168.1.1)  0.527 ms  0.612 ms  0.664 ms
 2  * * *
 3  * * *
 4  * * *
 5  * * *
 6  * * *
 7  * * *
 8  * * *
 9  * * *
10  * * *
11  * * *
12  * * *
13  * * *
14  * * *
15  * * *
16  * * *
17  * * *
18  * * *
19  * * *
20  * * *
21  * * *
22  * * *
23  * * *
24  * * *
25  * * *
26  * * *
27  * * *
28  * * *
29  * * *
30  * * *


root@gnolmir ~/i/regions (main)# traceroute -i enp1s0f2 34.81.202.211
traceroute to 34.81.202.211 (34.81.202.211), 30 hops max, 60 byte packets
 1  192.168.1.1 (192.168.1.1)  0.509 ms  0.592 ms  0.663 ms
 2  100.64.0.1 (100.64.0.1)  38.282 ms  38.302 ms  38.284 ms
 3  172.16.251.90 (172.16.251.90)  38.327 ms  62.204 ms  62.264 ms
 4  undefined.hostname.localhost (206.224.65.204)  62.239 ms undefined.hostname.localhost (206.224.65.200)  62.235 ms undefined.hostname.localhost (206.224.65.204)  62.253 ms
 5  undefined.hostname.localhost (206.224.65.188)  62.059 ms undefined.hostname.localhost (206.224.65.180)  62.091 ms undefined.hostname.localhost (206.224.65.186)  62.066 ms
 6  149.19.109.49 (149.19.109.49)  70.044 ms  58.183 ms  66.015 ms
 7  * * *
 8  * * *
 9  * * *
10  * * *
11  * * *
12  * * *
13  * * *
14  * * *
15  * * *
16  * * *
17  * * *
18  * * *
19  * * *
20  * * *
21  * * *
22  * * *
23  * * *
24  * * *
25  * * *
26  * * *
27  * * *
28  * * *
29  * * *
30  * * *
```

+ start visualizing what happens when we reach a target
    + create a networkx graph
    + each router gets a node 
    + each google cloud region gets a node
    + trace edges as seen in a traceroute or straight outta my script
    + extend to use default traceroute or my python implementation
    + extend to support different protocols
    + extend to support whole traceroute (every hop)
    + repeat the measurements did last week without starlink, do we still go through New York?
+ do the same with another interface and check if traffic still goes through new york 
+ Check Ripe Atlas for data


started writing script `vis.py`, now we have an idea of every ip contacted

## extra

* I was convinced that the ground station could be in different continents, but this can't be true, we are connected to ground stations in central europe (or at least GS a satellite can "see").


This guy suggests a way to identify GSs: https://www.reddit.com/r/Starlink/comments/plu96u/identifying_my_ground_stations_using_starlinks/

+ write a very simple script that makes measurements we need we can ask people on reddit to run for us (maybe inserting into a sqlite db they can send us so it is easier). A python public project could be enough, maybe for easeness of usage we can also package it and upload it on pypi so they just have to pip install and run it.

### list of geolocated ips 

+ https://www.gstatic.com/ipranges/cloud.json
+ https://ip-ranges.amazonaws.com/ip-ranges.json
+ https://www.microsoft.com/en-us/download/details.aspx?id=53601
+ https://geoip.linode.com/
+ https://digitalocean.com/geo/google.csv
+ https://www.alibabacloud.com/help/en/data-transmission-service/latest/whitelist-dts-ip-ranges-for-your-user-created-database
+ https://cloud.ibm.com/docs/cloud-infrastructure?topic=cloud-infrastructure-ibm-cloud-ip-ranges
+ https://docs.oracle.com/en-us/iaas/tools/public_ip_ranges.json --> incredibily transparent, consider using these 

huge problem with cloud providers -> we lose track of the packet as soon as it enters their network (:shrug)

## idk

1 hour reader 
bgpreader -w 1681562110,1681565710 -p ris -a 14593 is saved in `ris-dump-1h.txt`

this does not work bgpreader -w 1681562110,1681565710 -p routeviews -j 14593 for some reason


# 09/05 -> 16/05 

+ pick 5 geo distributed targets from: AWS Azure and Oracle
+ run traceroutes each 10 minutes TCP UDP ICMP for each one of them, let' s start with Ipv4 only
    + store them in 3 different directories (aws, azure, oracle)
    + each traceroute in a different file, naming schema `scope-ip-protocol-timestamp-starlink`
    + visualize this smaller amount of data

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
saving the traceroutes in `/home/rc/idp-castellotti-data/new-traceroutes`


I added 127.0.0.1 gnolmir in /etc/hosts https://askubuntu.com/a/458057
 
let's switch back to tracerouting universities, seems we can get more information (see almost every hop) , setting up another systemd-timer


```bash
jupyter notebook --NotebookApp.allow_origin=* --NotebookApp.allow_remote_access=1 --allow-root
```
```
ssh -D 9981 -J casr@sshgw.net.in.tum.de root@starlink.net.in.tum.de -p 10022
```
on browser with proxy set up:

[http://0.0.0.0:8888/notebooks/vis.ipynb](http://0.0.0.0:8888/notebooks/vis.ipynb)



# 16/05 -> 23/05

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



```
1 (git)-[master] % ./grpc_cli ls 192.168.100.1:9200 SpaceX.API.Device.Device -l                                                                                                    87 2 pts/5 ~/grpc/cmake/build rc@gnolmir 23-05-25 20:57:33
filename: spacex/api/device/device.proto
package: SpaceX.API.Device;
service Device {
  rpc Stream(stream SpaceX.API.Device.ToDevice) returns (stream SpaceX.API.Device.FromDevice) {}
  rpc Handle(SpaceX.API.Device.Request) returns (SpaceX.API.Device.Response) {}
}
```

```
(git)-[master] % ./grpc_cli type 192.168.100.1:9200 SpaceX.API.Device.Response                                                                                                   89 2 pts/5 ~/grpc/cmake/build rc@gnolmir 23-05-25 20:59:59
message Response {
  uint64 id = 1 [json_name = "id"];
  .SpaceX.API.Status.Status status = 2 [json_name = "status"];
  uint64 api_version = 3 [json_name = "apiVersion"];
  oneof response {
    .SpaceX.API.Device.GetNextIdResponse get_next_id = 1006 [json_name = "getNextId"];
    .SpaceX.API.Device.EnableDebugTelemResponse enable_debug_telem = 1034 [json_name = "enableDebugTelem"];
    .SpaceX.API.Device.FactoryResetResponse factory_reset = 1011 [json_name = "factoryReset"];
    .SpaceX.API.Device.GetDeviceInfoResponse get_device_info = 1004 [json_name = "getDeviceInfo"];
    .SpaceX.API.Device.GetLogResponse get_log = 1012 [json_name = "getLog"];
    .SpaceX.API.Device.GetNetworkInterfacesResponse get_network_interfaces = 1015 [json_name = "getNetworkInterfaces"];
    .SpaceX.API.Device.GetPingResponse get_ping = 1009 [json_name = "getPing"];
    .SpaceX.API.Device.PingHostResponse ping_host = 1016 [json_name = "pingHost"];
    .SpaceX.API.Device.RebootResponse reboot = 1001 [json_name = "reboot"];
    .SpaceX.API.Device.SpeedTestResponse speed_test = 1003 [json_name = "speedTest"];
    .SpaceX.API.Device.SetSkuResponse set_sku = 1013 [json_name = "setSku"];
    .SpaceX.API.Device.SetTrustedKeysResponse set_trusted_keys = 1010 [json_name = "setTrustedKeys"];
    .SpaceX.API.Device.UpdateResponse update = 1014 [json_name = "update"];
    .SpaceX.API.Device.GetLocationResponse get_location = 1017 [json_name = "getLocation"];
    .SpaceX.API.Device.GetHeapDumpResponse get_heap_dump = 1019 [json_name = "getHeapDump"];
    .SpaceX.API.Device.RestartControlResponse restart_control = 1020 [json_name = "restartControl"];
    .SpaceX.API.Device.FuseResponse fuse = 1021 [json_name = "fuse"];
    .SpaceX.API.Device.GetConnectionsResponse get_connections = 1023 [json_name = "getConnections"];
    .SpaceX.API.Device.StartSpeedtestResponse start_speedtest = 1027 [json_name = "startSpeedtest"];
    .SpaceX.API.Device.GetSpeedtestStatusResponse get_speedtest_status = 1028 [json_name = "getSpeedtestStatus"];
    .SpaceX.API.Device.ReportClientSpeedtestResponse report_client_speedtest = 1029 [json_name = "reportClientSpeedtest"];
    .SpaceX.API.Device.InitiateRemoteSshResponse initiate_remote_ssh = 1030 [json_name = "initiateRemoteSsh", deprecated = true];
    .SpaceX.API.Device.SelfTestResponse self_test = 1031 [json_name = "selfTest"];
    .SpaceX.API.Device.SetTestModeResponse set_test_mode = 1032 [json_name = "setTestMode"];
    .SpaceX.API.Device.SoftwareUpdateResponse software_update = 1033 [json_name = "softwareUpdate"];
    .SpaceX.API.Device.DishAuthenticateResponse dish_authenticate = 2005 [json_name = "dishAuthenticate"];
    .SpaceX.API.Device.DishGetContextResponse dish_get_context = 2003 [json_name = "dishGetContext"];
    .SpaceX.API.Device.DishGetHistoryResponse dish_get_history = 2006 [json_name = "dishGetHistory"];
    .SpaceX.API.Device.DishGetStatusResponse dish_get_status = 2004 [json_name = "dishGetStatus"];
    .SpaceX.API.Device.DishGetObstructionMapResponse dish_get_obstruction_map = 2008 [json_name = "dishGetObstructionMap"];
    .SpaceX.API.Device.DishStowResponse dish_stow = 2002 [json_name = "dishStow"];
    .SpaceX.API.Device.StartDishSelfTestResponse start_dish_self_test = 2012 [json_name = "startDishSelfTest"];
    .SpaceX.API.Device.DishSetEmcResponse dish_set_emc = 2007 [json_name = "dishSetEmc"];
    .SpaceX.API.Device.DishGetEmcResponse dish_get_emc = 2009 [json_name = "dishGetEmc"];
    .SpaceX.API.Device.DishSetConfigResponse dish_set_config = 2010 [json_name = "dishSetConfig"];
    .SpaceX.API.Device.DishGetConfigResponse dish_get_config = 2011 [json_name = "dishGetConfig"];
    .SpaceX.API.Device.DishInhibitGpsResponse dish_inhibit_gps = 2013 [json_name = "dishInhibitGps"];
    .SpaceX.API.Device.TransceiverIFLoopbackTestResponse transceiver_if_loopback_test = 4001 [json_name = "transceiverIfLoopbackTest"];
    .SpaceX.API.Device.TransceiverGetStatusResponse transceiver_get_status = 4003 [json_name = "transceiverGetStatus"];
    .SpaceX.API.Device.TransceiverGetTelemetryResponse transceiver_get_telemetry = 4004 [json_name = "transceiverGetTelemetry"];
    .SpaceX.API.Device.WifiAuthenticateResponse wifi_authenticate = 3005 [json_name = "wifiAuthenticate"];
    .SpaceX.API.Device.WifiGetClientsResponse wifi_get_clients = 3002 [json_name = "wifiGetClients"];
    .SpaceX.API.Device.WifiGetDiagnosticsResponse wifi_get_diagnostics = 3008 [json_name = "wifiGetDiagnostics"];
    .SpaceX.API.Device.WifiGetHistoryResponse wifi_get_history = 3006 [json_name = "wifiGetHistory"];
    .SpaceX.API.Device.WifiGetPingMetricsResponse wifi_get_ping_metrics = 3007 [json_name = "wifiGetPingMetrics"];
    .SpaceX.API.Device.WifiGetStatusResponse wifi_get_status = 3004 [json_name = "wifiGetStatus"];
    .SpaceX.API.Device.WifiSetConfigResponse wifi_set_config = 3001 [json_name = "wifiSetConfig"];
    .SpaceX.API.Device.WifiGetConfigResponse wifi_get_config = 3009 [json_name = "wifiGetConfig"];
    .SpaceX.API.Device.WifiSetupResponse wifi_setup = 3003 [json_name = "wifiSetup"];
    .SpaceX.API.Device.WifiGetPersistentStatsResponse wifi_get_persistent_stats = 3022 [json_name = "wifiGetPersistentStats"];
    .SpaceX.API.Device.WifiSetMeshDeviceTrustResponse wifi_set_mesh_device_trust = 3012 [json_name = "wifiSetMeshDeviceTrust"];
    .SpaceX.API.Device.WifiSetMeshConfigResponse wifi_set_mesh_config = 3013 [json_name = "wifiSetMeshConfig", deprecated = true];
    .SpaceX.API.Device.WifiGetClientHistoryResponse wifi_get_client_history = 3015 [json_name = "wifiGetClientHistory"];
    .SpaceX.API.Device.WifiSelfTestResponse wifi_self_test = 3016 [json_name = "wifiSelfTest"];
  }
  reserved 1018, 1026, 2025, 3011, 3014;
}
```


```javascript=
 proto.SpaceX.API.Device.DishGetContextResponse.serializeBinaryToWriter = function (e, t) {
        var o = void 0;
        null != (o = e.getDeviceInfo()) && t.writeMessage(1, o, n.DeviceInfo.serializeBinaryToWriter),
        null != (o = e.getDeviceState()) && t.writeMessage(7, o, n.DeviceState.serializeBinaryToWriter),
        0 !== (o = e.getObstructionFraction()) && t.writeFloat(2, o),
        0 !== (o = e.getObstructionValidS()) && t.writeFloat(3, o),
        (o = e.getObstructionCurrent()) && t.writeBool(12, o),
        0 !== (o = e.getCellId()) && t.writeUint32(4, o),
        0 !== (o = e.getPopRackId()) && t.writeUint32(5, o),
        0 !== (o = e.getInitialSatelliteId()) && t.writeUint32(8, o),
        0 !== (o = e.getInitialGatewayId()) && t.writeUint32(9, o),
        (o = e.getOnBackupBeam()) && t.writeBool(10, o),
        0 !== (o = e.getSecondsToSlotEnd()) && t.writeFloat(6, o),
        (o = e.getDebugTelemetryEnabled()) && t.writeBool(11, o),
        0 !== (o = e.getPopPingDropRate15sMean()) && t.writeFloat(13, o),
        0 !== (o = e.getPopPingLatencyMs15sMean()) && t.writeFloat(14, o),
        0 !== (o = e.getSecondsSinceLast1sOutage()) && t.writeFloat(15, o),
        0 !== (o = e.getSecondsSinceLast2sOutage()) && t.writeFloat(16, o),
        0 !== (o = e.getSecondsSinceLast5sOutage()) && t.writeFloat(17, o),
        0 !== (o = e.getSecondsSinceLast15sOutage()) && t.writeFloat(18, o),
        0 !== (o = e.getSecondsSinceLast60sOutage()) && t.writeFloat(19, o)
      },
```


grpcurl -plaintext  -d '{"dishGetConfig":{}}' 192.168.100.1:9200 SpaceX.API.Device.Device/Handle
{
  "apiVersion": "7",
  "dishGetConfig": {
    "dishConfig": {
      "applySnowMeltMode": true,
      "applyLocationRequestMode": true,
      "applyLevelDishMode": true,
      "applyPowerSaveStartMinutes": true,
      "applyPowerSaveDurationMinutes": true,
      "applyPowerSaveMode": true
    }
  }
}




rc@gnolmir ~/idp-castellotti (main) [127]> grpcurl -plaintext  -d '{"dishGetContext":{}}' 192.168.100.1:9200 SpaceX.API.Device.Device/Handle
ERROR:
  Code: PermissionDenied
  Message: Permission denied
  
  
 grpcurl -plaintext  -d '{"get_status":{}}' 192.168.100.1:9200 SpaceX.API.Device.Device/Handle
  
  
  
  rc@gnolmir ~/idp-castellotti (main) [1]> ../grpc/cmake/build/grpc_cli ls 192.168.100.1:9200
SpaceX.API.Device.Device
grpc.reflection.v1alpha.ServerReflection

## 30/05 -->
+ start filtering "visible satellites" by distance, prolly ~800km
+ download a big chonky file (` wget -4 https://speed.hetzner.de/10GB.bin --report-speed=bits -O /dev/null --bind-address 192.168.1.196`) 





### Get info about bandwidth/ping latency

grpcurl -plaintext -d '{"get_status":{}}' 192.168.100.1:9200 SpaceX.API.Device.Device/Handle | jq ".dishGetStatus.downlinkThroughputBps"

grpcurl -plaintext -d '{"get_status":{}}' 192.168.100.1:9200 SpaceX.API.Device.Device/Handle | jq ".dishGetStatus.popPingLatencyMs"




































## setup something to download a large file to measure latency



from starlink_grpc import status_data
pop_ping_latency_ms=status_data()[0]["pop_ping_latency_ms"]
print(pop_ping_latency_ms)



correlate get_status downlink_throughput_bps with other stuff from download
if something strange happens 

plot satellites on y axis (draw a line to represent how much time do we see that satellite for)


how much time for satellite? 

increase the distance and check how many satellites we see?


check how much the satellite numbers dec increasing the distance 









visible_satellites:
+ 



set route for speed hetzener

ip route
default via 131.159.14.190 dev enp3s0 proto dhcp src 131.159.14.181 metric 10 
default via 192.168.1.1 dev enp1s0f3 proto dhcp src 192.168.1.228 metric 1024 
default via 192.168.200.11 dev enp1s0f2 proto dhcp src 192.168.200.14 metric 1024 
131.159.14.128/26 dev enp3s0 proto kernel scope link src 131.159.14.181 
131.159.14.190 dev enp3s0 proto dhcp scope link src 131.159.14.181 metric 10 
192.168.1.0/24 dev enp1s0f3 proto kernel scope link src 192.168.1.228 
192.168.1.1 dev enp1s0f3 proto dhcp scope link src 192.168.1.228 metric 1024 
192.168.100.1 via 192.168.200.11 dev enp1s0f2 proto dhcp metric 9 
192.168.200.0/24 dev enp1s0f2 proto kernel scope link src 192.168.200.14 
192.168.200.11 dev enp1s0f2 proto dhcp scope link src 192.168.200.14 metric 1024 
rc@gnolmir ~/idp-castellotti (main)> sudo ip route add 88.198.248.254 via 192.168.200.11




ifstat -n -w -i enp1s0f2 | stdbuf -oL tr -s " " "," | stdbuf -oL cut -c2- | tail -n +3 


to get speed from ifstat





restoring route sudo ip route add 192.168.100.1 via 192.168.1.1


## todo
+ create a timeseries
    + y: a satellite and how much time do we see it for (line)
    + we approach this in this way: we collect all satellites each minute for 10 minutes
    + 
plot satellites on y axis (draw a line to represent how much time do we see that satellite for)


how much time for satellite? 

increase the distance and check how many satellites we see?


check how much the satellite numbers dec increasing the distance 




## starting to cleanup
+ explain how we obtained the targets in the data repo



## satellites

```sql	
SELECT satname, start_timestamp, end_timestamp
FROM satellites
WHERE satname LIKE 'STARLINK-%'
GROUP BY satname
HAVING COUNT(*) >=4
ORDER BY satname;
```


started: 2023-06-16 14:49:16.055117
ended: 2023-06-18 10:58:55.304417







# grpc api

### first of all let's document the starlink api

####  grpcurl -plaintext 192.168.100.1:9200 describe

```bash=
rc@gnolmir ~> grpcurl -plaintext 192.168.100.1:9200 describe
SpaceX.API.Device.Device is a service:
service Device {
  rpc Handle ( .SpaceX.API.Device.Request ) returns ( .SpaceX.API.Device.Response );
  rpc Stream ( stream .SpaceX.API.Device.ToDevice ) returns ( stream .SpaceX.API.Device.FromDevice );
}
grpc.reflection.v1alpha.ServerReflection is a service:
service ServerReflection {
  rpc ServerReflectionInfo ( stream .grpc.reflection.v1alpha.ServerReflectionRequest ) returns ( stream .grpc.reflection.v1alpha.ServerReflectionResponse );
}
```
#### grpcurl -plaintext 192.168.100.1:9200 describe SpaceX.API.Device.Request

```bash=
rc@gnolmir ~> grpcurl -plaintext 192.168.100.1:9200 describe SpaceX.API.Device.Request
SpaceX.API.Device.Request is a message:
message Request {
  uint64 id = 1;
  string target_id = 13;
  uint64 epoch_id = 14;
  oneof request {
    .SpaceX.API.Device.SignedData signed_request = 15;
    .SpaceX.API.Device.RebootRequest reboot = 1001;
    .SpaceX.API.Device.SpeedTestRequest speed_test = 1003;
    .SpaceX.API.Device.GetStatusRequest get_status = 1004;
    .SpaceX.API.Device.AuthenticateRequest authenticate = 1005;
    .SpaceX.API.Device.GetNextIdRequest get_next_id = 1006;
    .SpaceX.API.Device.GetHistoryRequest get_history = 1007;
    .SpaceX.API.Device.GetDeviceInfoRequest get_device_info = 1008;
    .SpaceX.API.Device.GetPingRequest get_ping = 1009;
    .SpaceX.API.Device.SetTrustedKeysRequest set_trusted_keys = 1010;
    .SpaceX.API.Device.FactoryResetRequest factory_reset = 1011;
    .SpaceX.API.Device.GetLogRequest get_log = 1012;
    .SpaceX.API.Device.SetSkuRequest set_sku = 1013;
    .SpaceX.API.Device.UpdateRequest update = 1014;
    .SpaceX.API.Device.GetNetworkInterfacesRequest get_network_interfaces = 1015;
    .SpaceX.API.Device.PingHostRequest ping_host = 1016;
    .SpaceX.API.Device.GetLocationRequest get_location = 1017;
    .SpaceX.API.Device.GetHeapDumpRequest get_heap_dump = 1019;
    .SpaceX.API.Device.RestartControlRequest restart_control = 1020;
    .SpaceX.API.Device.FuseRequest fuse = 1021;
    .SpaceX.API.Device.GetPersistentStatsRequest get_persistent_stats = 1022;
    .SpaceX.API.Device.GetConnectionsRequest get_connections = 1023;
    .SpaceX.API.Device.StartSpeedtestRequest start_speedtest = 1027;
    .SpaceX.API.Device.GetSpeedtestStatusRequest get_speedtest_status = 1028;
    .SpaceX.API.Device.ReportClientSpeedtestRequest report_client_speedtest = 1029;
    .SpaceX.API.Device.InitiateRemoteSshRequest initiate_remote_ssh = 1030 [deprecated = true];
    .SpaceX.API.Device.SelfTestRequest self_test = 1031;
    .SpaceX.API.Device.SetTestModeRequest set_test_mode = 1032;
    .SpaceX.API.Device.SoftwareUpdateRequest software_update = 1033;
    .SpaceX.API.Device.EnableDebugTelemRequest enable_debug_telem = 1034;
    .SpaceX.API.Device.DishStowRequest dish_stow = 2002;
    .SpaceX.API.Device.DishGetContextRequest dish_get_context = 2003;
    .SpaceX.API.Device.DishSetEmcRequest dish_set_emc = 2007;
    .SpaceX.API.Device.DishGetObstructionMapRequest dish_get_obstruction_map = 2008;
    .SpaceX.API.Device.DishGetEmcRequest dish_get_emc = 2009;
    .SpaceX.API.Device.DishSetConfigRequest dish_set_config = 2010;
    .SpaceX.API.Device.DishGetConfigRequest dish_get_config = 2011;
    .SpaceX.API.Device.StartDishSelfTestRequest start_dish_self_test = 2012;
    .SpaceX.API.Device.DishPowerSaveRequest dish_power_save = 2013;
    .SpaceX.API.Device.DishInhibitGpsRequest dish_inhibit_gps = 2014;
    .SpaceX.API.Device.WifiSetConfigRequest wifi_set_config = 3001;
    .SpaceX.API.Device.WifiGetClientsRequest wifi_get_clients = 3002;
    .SpaceX.API.Device.WifiSetupRequest wifi_setup = 3003;
    .SpaceX.API.Device.WifiGetPingMetricsRequest wifi_get_ping_metrics = 3007;
    .SpaceX.API.Device.WifiGetDiagnosticsRequest wifi_get_diagnostics = 3008;
    .SpaceX.API.Device.WifiGetConfigRequest wifi_get_config = 3009;
    .SpaceX.API.Device.WifiSetMeshDeviceTrustRequest wifi_set_mesh_device_trust = 3012;
    .SpaceX.API.Device.WifiSetMeshConfigRequest wifi_set_mesh_config = 3013 [deprecated = true];
    .SpaceX.API.Device.WifiGetClientHistoryRequest wifi_get_client_history = 3015;
    .SpaceX.API.Device.WifiSetAviationConformedRequest wifi_set_aviation_conformed = 3016;
    .SpaceX.API.Device.WifiSetClientGivenNameRequest wifi_set_client_given_name = 3017;
    .SpaceX.API.Device.WifiSelfTestRequest wifi_self_test = 3018;
    .SpaceX.API.Device.TransceiverIFLoopbackTestRequest transceiver_if_loopback_test = 4001;
    .SpaceX.API.Device.TransceiverGetStatusRequest transceiver_get_status = 4003;
    .SpaceX.API.Device.TransceiverGetTelemetryRequest transceiver_get_telemetry = 4004;
  }
  reserved 1018, 1025, 1026, 3011, 3014;
}
```

#### grpcurl -plaintext 192.168.100.1:9200 describe SpaceX.API.Device.Response

```bash=
rc@gnolmir ~> grpcurl -plaintext 192.168.100.1:9200 describe SpaceX.API.Device.Response
SpaceX.API.Device.Response is a message:
message Response {
  uint64 id = 1;
  .SpaceX.API.Status.Status status = 2;
  uint64 api_version = 3;
  oneof response {
    .SpaceX.API.Device.RebootResponse reboot = 1001;
    .SpaceX.API.Device.SpeedTestResponse speed_test = 1003;
    .SpaceX.API.Device.GetDeviceInfoResponse get_device_info = 1004;
    .SpaceX.API.Device.GetNextIdResponse get_next_id = 1006;
    .SpaceX.API.Device.GetPingResponse get_ping = 1009;
    .SpaceX.API.Device.SetTrustedKeysResponse set_trusted_keys = 1010;
    .SpaceX.API.Device.FactoryResetResponse factory_reset = 1011;
    .SpaceX.API.Device.GetLogResponse get_log = 1012;
    .SpaceX.API.Device.SetSkuResponse set_sku = 1013;
    .SpaceX.API.Device.UpdateResponse update = 1014;
    .SpaceX.API.Device.GetNetworkInterfacesResponse get_network_interfaces = 1015;
    .SpaceX.API.Device.PingHostResponse ping_host = 1016;
    .SpaceX.API.Device.GetLocationResponse get_location = 1017;
    .SpaceX.API.Device.GetHeapDumpResponse get_heap_dump = 1019;
```bash=
rc@gnolmir:~$ grpcurl -plaintext -d '{"set_test_mode":{}}' 192.168.100.1:9200 SpaceX.API.Device.Device/Handle
ERROR:
  Code: PermissionDenied
  Message: Permission denied
  ```




query 
timestamp -> list of visible satellites





# visible satellites

```sql=
sqlite> select * from satellites limit 10;
1|1|1687289189.53788|STARLINK-1360|69deg 38' 55.8"|158deg 48' 05.1"
2|1|1687289189.53788|STARLINK-2095|43deg 57' 23.2"|02deg 23' 36.7"
3|1|1687289189.53788|STARLINK-2617|53deg 48' 58.5"|343deg 49' 50.9"
4|1|1687289189.53788|STARLINK-3277|40deg 16' 40.7"|211deg 35' 26.7"
5|1|1687289189.53788|STARLINK-3846|47deg 57' 52.3"|26deg 55' 01.4"
6|1|1687289189.53788|STARLINK-4721|56deg 52' 34.4"|159deg 59' 15.2"
7|1|1687289189.53788|STARLINK-5599|58deg 39' 41.2"|309deg 43' 10.5"
8|1|1687289189.53788|STARLINK-5584|59deg 32' 14.8"|276deg 44' 23.1"
9|1|1687289189.53788|STARLINK-5557|60deg 04' 25.1"|295deg 58' 25.2"
10|1|1687289189.53788|STARLINK-5591|54deg 03' 30.8"|327deg 24' 34.7"
```

```sql=
sqlite> select * from satellites where satname='STARLINK-1360';
1|1|1687289189.53788|STARLINK-1360|69deg 38' 55.8"|158deg 48' 05.1"
21|2|1687289206.13395|STARLINK-1360|73deg 07' 10.2"|121deg 56' 36.6"
41|3|1687289222.94262|STARLINK-1360|68deg 58' 52.2"|86deg 03' 21.7"
62|4|1687289239.51901|STARLINK-1360|61deg 03' 57.2"|67deg 20' 49.5"
80|5|1687289256.15036|STARLINK-1360|52deg 52' 05.5"|57deg 49' 38.2"
98|6|1687289272.62732|STARLINK-1360|45deg 34' 06.9"|52deg 22' 33.8"
18575|2640|1687332133.47345|STARLINK-1360|46deg 06' 29.6"|324deg 21' 20.2"
18581|2641|1687332149.65512|STARLINK-1360|53deg 55' 06.2"|323deg 47' 20.2"
18586|2642|1687332166.01547|STARLINK-1360|63deg 24' 39.9"|322deg 42' 29.8"
18591|2643|1687332182.16873|STARLINK-1360|74deg 14' 38.6"|320deg 00' 24.1"
18598|2644|1687332198.6235|STARLINK-1360|86deg 08' 40.7"|299deg 16' 59.4"
18604|2645|1687332214.77809|STARLINK-1360|80deg 59' 32.9"|157deg 21' 36.1"
18611|2646|1687332231.23122|STARLINK-1360|69deg 17' 30.6"|150deg 53' 51.9"
18618|2647|1687332247.41196|STARLINK-1360|59deg 03' 02.1"|149deg 11' 42.7"
18625|2648|1687332263.85792|STARLINK-1360|50deg 16' 28.3"|148deg 23' 37.4"
18634|2649|1687332280.09123|STARLINK-1360|43deg 04' 05.8"|147deg 56' 03.3"
```
```json=
{'STARLINK-1360': [(datetime.datetime(2023, 6, 20, 21, 26, 30), datetime.datetime(2023, 6, 20, 21, 27, 53)), 
                   (datetime.datetime(2023, 6, 21, 9, 22, 13), datetime.datetime(2023, 6, 21, 9, 24, 40))
                  ]
}
```



### censys
ireallylovebear@proton.me
hXqAx923GbrUq3


api id: 
api secret: 




curl -g -X 'GET' \
                     'https://search.censys.io/api/v2/hosts/search?per_page=25&virtual_hosts=EXCLUDE&q=autonomous_system.name%3D%60SPACEX-STARLINK%60' \
                     -H 'Accept: application/json' \
                     --user "712b60f2-e085-421c-9522-3a0e439a01db:8O0mKavMseWgYFPNMhBVF6e9Vl4RmEfz"
                     
                     
                     
                     
we should now be able to extract obstruction maps and to track satellites, it should be interesting to extract a map each second for 5 minutes and save it, we can then export it to seaborn and save it as png, let's try that

                     
                     
             
             

```
while true; do wget -4 https://speed.hetzner.de/10GB.bin --report-speed=bits -O /dev/null; done
sudo ip route add 88.198.248.254  via 192.168.1.1
while true; do wget -4  http://ftp.de.debian.org/debian-cd/current/amd64/iso-dvd/debian-12.0.0-amd64-DVD-1.iso --report-speed=bits -O /dev/null; done
while true; do wget -4  http://mirror.netcologne.de/debian-cd/current/amd64/iso-dvd/debian-12.0.0-amd64-DVD-1.iso --report-speed=bits -O /dev/null; done
while true; do wget -4  http://mirror.23media.com//debian-cd/current/amd64/iso-dvd/debian-12.0.0-amd64-DVD-1.iso --report-speed=bits -O /dev/null; done
http://mirror.23media.com//debian-cd/current/amd64/iso-dvd/debian-12.0.0-amd
`````





sudo python3 cloud-traceroutes.py -d prova6 -a ../idp-castellotti-data/ipasn_20230315.dat -r ../idp-castellotti-data/targets6.csv
