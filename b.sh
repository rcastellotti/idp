#!/bin/bash

set -xe

iperf3 -c 138.246.253.20 -u -b  10k -t  300
iperf3 -c 138.246.253.20 -u -b  20k -t  300
iperf3 -c 138.246.253.20 -u -b  50k -t  300
iperf3 -c 138.246.253.20 -u -b 100k -t  300
iperf3 -c 138.246.253.20 -u -b   1M -t  300
iperf3 -c 138.246.253.20 -u -b  10M -t  300
