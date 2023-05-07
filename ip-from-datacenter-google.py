# this script takes one ip from the prefix for each region and saves it to file

import json
import requests
import ipaddress
import random

# Fetch the JSON data from the URL
url = "https://www.gstatic.com/ipranges/cloud.json"
response = requests.get(url)
data = json.loads(response.text)
datone = {}
just_one = []
datone["syncToken"] = data["syncToken"]
datone["creationTime"] = data["creationTime"]
datone["prefixes"] = []
# Loop through each item in the "prefixes" list and replace the "prefix" field with a random IP address inside that network
for prefix in data["prefixes"]:
    if prefix["scope"] not in just_one:
        if "ipv4Prefix" in prefix:
            ip_network = ipaddress.ip_network(prefix["ipv4Prefix"])
            random_ip = ipaddress.IPv4Address(
                random.randint(
                    int(ip_network.network_address) + 1,
                    int(ip_network.broadcast_address) - 1,
                )
            )
            prefix["ip"] = str(random_ip)
        elif "ipv6Prefix" in prefix:
            ip_network = ipaddress.ip_network(prefix["ipv6Prefix"])
            random_ip = ipaddress.IPv6Address(
                random.randint(
                    int(ip_network.network_address) + 1,
                    int(ip_network.broadcast_address) - 1,
                )
            )
            prefix["ip"] = str(random_ip)
        just_one.append(prefix["scope"])
        datone["prefixes"].append(prefix)

# Output the modified JSON data
with open("cloud-ips.json", "w+") as f:
    f.write(json.dumps(datone, indent=4))
