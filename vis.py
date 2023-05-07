# this script will help us visualize various things, first of all let's extract all ips we contact

import os
import csv
import pprint
stats={}

base="/root/idp-castellotti-data/regions-oracle-traceroute/"
    
for file in os.listdir(base):
    filename = os.fsdecode(file)
    if "starlink" in filename:
        with open(base+filename, newline='') as csvfile:
            reader = csv.reader(csvfile, quotechar='|')
            for row in reader:
                ip=row[2]
                if ip !="*" and ip !="ip" and ip !="???":
                    if ip not in stats:
                        stats[ip] ={"count":1,"hostname":row[3],"asn":row[4]}
                    stats[ip]["count"]+=1
# pprint.pprint(stats)
print(stats)


with open('dict.csv', 'w') as csv_file:  
    writer = csv.writer(csv_file)
    for key, value in stats.items():
       writer.writerow([key, value["count"],value["hostname"],value["asn"]])



# first of all let's try to visualize 
# essenzialmente dobbiamo prendere tutti gli ip e piazzarli su un grafo
# dopo andiamo per ogni file riga per riga, e colleghiamo ogni hop con il successivo
