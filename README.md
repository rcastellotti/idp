# IDP Castellotti

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

## additional stuff

+ http://geoip.starlinkisp.net/feed.csv
+ get pops: `curl -g -X 'GET' \
'https://search.censys.io/api/v2/hosts/search?per_page=25&virtual_hosts=EXCLUDE&q=autonomous_system.name%3D%60SPACEX-STARLINK%60+and+dns.reverse_dns.names+%3Dcustomer.*' \
-H 'Accept: application/json' \
--user "$CENSYS_API_ID:$CENSYS_API_SECRET"`