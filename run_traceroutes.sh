#!/bin/bash
# a simple script to run some traceroutes
targets=("caida.org" "utu.fi" "garr.it" "tum.de" "mit.edu")
date=$(date +"%Y-%m-%dT%H:%M:%S")
mkdir -p traceroutes/$date
for target in "${targets[@]}"
do
    traceroute -A -i enp3s0 $target >> traceroutes/${date}/traceroute_default_${target}_${date}.txt
    traceroute -A -i enp3s0 -T $target >> traceroutes/${date}/traceroute_default_tcp_${target}_${date}.txt
    traceroute -A -i enp3s0 -4 $target >> traceroutes/${date}/traceroute_default_ipv4_${target}_${date}.txt
    traceroute -A -i enp3s0 -6 $target >> traceroutes/${date}/traceroute_default_ipv6_${target}_${date}.txt
    traceroute -A -i enp1s0f2 $target >> traceroutes/${date}/traceroute_starlink_${target}_${date}.txt
    traceroute -A -i enp1s0f2 -T $target >> traceroutes/${date}/traceroute_starlink_tcp_${target}_${date}.txt
    traceroute -A -i enp1s0f2 -4 $target >> traceroutes/${date}/traceroute_starlink_ipv4_${target}_${date}.txt
    traceroute -A -i enp1s0f2 -6 $target >> traceroutes/${date}/traceroute_starlink_ipv6_${target}_${date}.txt
done