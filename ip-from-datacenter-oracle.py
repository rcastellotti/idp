# this script takes one ip from the prefix for each region and saves it to file

import json
import requests
import ipaddress
import random

# Fetch the JSON data from the URL
url = "https://docs.oracle.com/en-us/iaas/tools/public_ip_ranges.json"
response = requests.get(url)
data = json.loads(response.text)
datone = {}
just_one = []
datone["last_updated_timestamp"] = data["last_updated_timestamp"]
datone["prefixes"] = []
for r in data["regions"]:
    pr={}
    ip_network = ipaddress.ip_network(random.choice(r["cidrs"])["cidr"])
    random_ip = ipaddress.IPv4Address(
        random.randint(
            int(ip_network.network_address) + 1,
            int(ip_network.broadcast_address) - 1,
        )
    )
    pr["scope"] = r["region"]
    pr["ip"] = str(random_ip)
    just_one.append(r["region"])
    datone["prefixes"].append(pr)

print(datone)
# Output the modified JSON data
with open("cloud-oracle-ips.json", "w+") as f:
    # f.write("a")
    json.dumps(datone,indent=4)
    f.write(json.dumps(datone, indent=4))