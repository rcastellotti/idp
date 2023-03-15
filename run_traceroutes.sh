#!/bin/bash
# a simple script to run some traceroutes
targets=("caida.org" "utu.fi" "garr.it" "tum.de" "mit.edu")
date=$(date +"%Y-%m-%dT%H:%M:%S")
mkdir -p traceroutes/$date
for target in "${targets[@]}"
do
    traceroute -i enp3s0 $target >> traceroutes/${date}/traceroute_default_${target}_${date}.txt
    traceroute -i enp1s0f2 $target >> traceroutes/${date}/traceroute_starlink_${target}_${date}.txt
done