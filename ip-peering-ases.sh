#!/bin/bash
# a simple script to check whether groundstations change
set -e 
# AS 1798 OREGON | oregon.gov
# AS 20932 SIG-ST - Services Industriels de Geneve | unige.ch
# AS 8426 CLARANET-AS - Claranet Limited | manchester.ac.uk
# AS 20811 BRENNERCOM-AS - Brennercom S.p.A. | uniroma1.it

tr() {
    echo "traceroute $1 $2"   
    echo "===ICMP==="
    traceroute -i enp1s0f2 -q 1 -n -I $1 
    traceroute -i enp1s0f2 -q 1 -n -I $2 
    echo "===UDP==="
    traceroute -i enp1s0f2 -q 1 -n -U $1 
    traceroute -i enp1s0f2 -q 1 -n -U $2  
    echo "===TCP==="
    traceroute -i enp1s0f2 -q 1 -n -T $1 
    traceroute -i enp1s0f2 -q 1 -n -T $2 
    echo ====
}


tr "192.149.16.194" "oregon.gov"
tr "185.68.206.75" "unige.ch"
tr "194.15.233.244" "manchester.ac.uk"
tr "95.171.35.164" "uniroma1.it"
