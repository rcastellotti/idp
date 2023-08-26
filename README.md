# IDP Castellotti

+ `common.py` ~> collection of miscellaneous functions
+ `nine981.py` ~> interact with the gRPC api the dish exposes
+ `cloud-traceroutes.py` ~> the tool to perform (and visualize) traceroutes to cloud datacenters
+ `s.py` ~> cli to use `nine918.py`
+ `map.py` ~> download obstruction maps for a certain amount of seconds (to get meaningful data remember to reboot first)
+ `viz.py` ~> a script to create images to visualize obstruction maps
+ `hand.py` ~> the tool to detect handovers (check `main.ipynb` to see a viz)
+ `visible-satellites.py` ~> extracts visible Starlink satellites (you get to define what "visible" means)
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
