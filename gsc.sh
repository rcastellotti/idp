#!/bin/bash
# a simple script to check whether groundstations change
set -e 
targets=("caida.org" "utu.fi" "garr.it" "tum.de" "mit.edu" "unibuc.ro" "ox.ac.uk" "cam.ac.uk" "www.uct.ac.za")
date=$(date +"%Y-%m-%dT%H:%M:%S")
for target in "${targets[@]}"
do
    mkdir -p /root/idp-castellotti-data/traceroutes_cgs/$target
    echo "traceroute ${target}"
    traceroute -U -i enp1s0f2 -n $target | tail -n+2 | awk '{ print $1 "," $2 }' >> /root/idp-castellotti-data/traceroutes_cgs/$target/udp_${date}.txt
    traceroute -T -i enp1s0f2 -n $target | tail -n+2 | awk '{ print $1 "," $2 }' >>  /root/idp-castellotti-data/traceroutes_cgs/$target/tcp_${date}.txt
    traceroute -I -i enp1s0f2 -n $target | tail -n+2 | awk '{ print $1 "," $2 }' >>  /root/idp-castellotti-data/traceroutes_cgs/$target/icmp_${date}.txt
    traceroute -U -i enp1s0f2 $target  >>  /root/idp-castellotti-data/traceroutes_cgs/$target/extended_udp_${date}.txt
    traceroute -T -i enp1s0f2  $target >>  /root/idp-castellotti-data/traceroutes_cgs/$target/extended_tcp_${date}.txt
    traceroute -I -i enp1s0f2  $target >>  /root/idp-castellotti-data/traceroutes_cgs/$target/extended_icmp_${date}.txt
done


