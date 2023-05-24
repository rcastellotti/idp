#!/bin/bash

trap echo 0
echo "timestamp,rtt"

ping $* | while read line; do

  [[ "$line" =~ ^PING ]] && continue
  [[ ! "$line" =~ "bytes from" ]] && continue

  rtt=${line##*time=}
  rtt=${rtt%% *}
  timestamp=$(date +%s)

  echo -n "$timestamp,$rtt"
  echo
done
    