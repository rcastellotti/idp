# IDP Castellotti


measure latency check still works after nine981 rename

## `api.py`
This module calls the gRPC api and returns JSON data, offers:
    + `api.get_status()`
    + `api.reboot()`
    + `api.get_obstruction_map()`
Should be straightforward to extend to call [other gRPC endpoints](https://gist.github.com/rcastellotti/e20630366dfeaeada6cc2680f562f6ac)

## `s.py`
An extremely simple CLI to call methods from the `api` module


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

given a directory of obstruction maps: 
TODO: give equivalent
<!-- 
# ffmpeg.input(f"{directory}-viz/*.png", framerate=60, pattern_type="glob").output(
#     args.output,
#     vcodec="libx264",
#     pix_fmt="yuv420p",
#     vf="pad=ceil(iw/2)*2:ceil(ih/2)*2",
# ).run() -->



+ maybe save obstruction maps visualization
+  common py listare tutto
+  + configure pyasn
+  + i think pop measure latency is useless

<!--  python3 obstruction_maps_visualization.py -i ../idp-castellotti-data/maps_overnight -o ./marco
 -->