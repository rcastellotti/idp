# IDP Castellotti

satellite obstruction maps visualization: <https://youtu.be/PjfMPr20suw>

explanation for some things that may be hardcoded:
+ `192.168.1.1` ~> default gateway for Starlink
+ `192.168.100.1` ~> API endpoint
+ `enp1s0f2` ~> Starlink interface (it changed after some reboots, rule of thumb: every hardcoded interface is Starlink's)
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

## additional resources

+ https://www.gstatic.com/ipranges/cloud.json
+ https://ip-ranges.amazonaws.com/ip-ranges.json
+ https://www.microsoft.com/en-us/download/details.aspx?id=53601
+ https://geoip.linode.com/
+ https://digitalocean.com/geo/google.csv
+ https://www.alibabacloud.com/help/en/data-transmission-service/latest/whitelist-dts-ip-ranges-for-your-user-created-database
+ https://cloud.ibm.com/docs/cloud-infrastructure?topic=cloud-infrastructure-ibm-cloud-ip-ranges
+ https://docs.oracle.com/en-us/iaas/tools/public_ip_ranges.json --> incredibily transparent, consider using these 
+ http://geoip.starlinkisp.net/feed.csv
+ https://lizizhikevich.github.io/assets/papers/LEO-HitchHiking.pdf (updated)
+ https://publicdata.caida.org/datasets/as-relationships/serial-1/20230401.as-rel.txt.bz2
