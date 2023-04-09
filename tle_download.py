# a simple script to download satellites list and convert it to json
import requests
import json

url = 'https://celestrak.org/NORAD/elements/gp.php?GROUP=starlink&FORMAT=tle'
r = requests.get(url, allow_redirects=True)
with open('satellites.txt', 'wb') as f:
    f.write(r.content)
    print("downloaded satellites list")
    
satellites=dict()
with open("satellites.txt", "r") as f:
    f=f.read().splitlines()
    for line_no, line in enumerate(f):
        if line_no%3 ==0:
            satellites[line.strip()]={"l1": f[line_no+1], "l2": f[line_no+2]}
            
json_object = json.dumps(satellites, indent=4)
with open("satellites.json", "w") as outfile:
    outfile.write(json_object)
    print("wrote satellites to satellites.json") 
