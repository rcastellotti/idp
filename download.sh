#!/bin/bash

url="https://speed.hetzner.de/10GB.bin"
output_file="output_file_name"
speed_file="speed.txt"

# Remove any existing speed file
rm -f "$speed_file"

# Start downloading the file
wget -O "$output_file" "$url" 2>&1 | awk '/[0-9.]+ [KM]B\/s/ {print substr($3, 1, length($3)-2)}' > "$speed_file"




