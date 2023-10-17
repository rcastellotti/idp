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


## traceroute systemd-timer

```bash
systemd-analyze verify traceroute.*
cp -r traceroute.* /etc/systemd/system/
systemctl daemon-reload
systemctl start traceroute
systemctl enable traceroute
systemctl status traceroute
journalctl -u traceroute
```

## geolocated ips

+ https://www.gstatic.com/ipranges/cloud.json
+ https://ip-ranges.amazonaws.com/ip-ranges.json
+ https://www.microsoft.com/en-us/download/details.aspx?id=53601
+ https://geoip.linode.com/
+ https://digitalocean.com/geo/google.csv
+ https://www.alibabacloud.com/help/en/data-transmission-service/latest/whitelist-dts-ip-ranges-for-your-user-created-database
+ https://cloud.ibm.com/docs/cloud-infrastructure?topic=cloud-infrastructure-ibm-cloud-ip-ranges
+ https://docs.oracle.com/en-us/iaas/tools/public_ip_ranges.json --> incredibily transparent, consider using these 

huge problem with cloud providers -> we loose track of the packet as soon as it enters their network

+ run `iperf3` to create some constant background noise to a target J. will setup
    + server: `iperf -s -u`
    + client: `iperf -c 138.246.253.20 -p 5001 -u -b 5k` 
+ running for some time: `sudo python3 traceroutes_stress.py` (saving results in `~/idp-castellotti/data/traceroutes-iperf-5bks`) (typo)


+ ping two hosts in the same geographic area but in different ASes (in particular one AS peering directly with SpaceX and one not peering directly) => meh


## additional stuff

+ http://geoip.starlinkisp.net/feed.csv
+ get pops: `curl -g -X 'GET' \
'https://search.censys.io/api/v2/hosts/search?per_page=25&virtual_hosts=EXCLUDE&q=autonomous_system.name%3D%60SPACEX-STARLINK%60+and+dns.reverse_dns.names+%3Dcustomer.*' \
-H 'Accept: application/json' \
--user "$CENSYS_API_ID:$CENSYS_API_SECRET"`