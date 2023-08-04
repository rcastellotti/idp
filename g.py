import json
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
from datetime import datetime 

def detect_handovers(dir):
    l = sorted(os.listdir(dir))
    print(f"[*] maps interval: {l[0][:-5]} and {l[-1][:-5]}")

    suspected_handovers = set()
    for i in range(0, len(l) - 1, 2):

        f1 = os.path.join(dir, l[i])
        f2 = os.path.join(dir, l[i + 1])

        map1 = json.load(open(f1))
        map1 = map1["dishGetObstructionMap"]["snr"]
        map1 = np.array(map1).reshape(123, 123)
        map2 = json.load(open(f2))
        map2 = map2["dishGetObstructionMap"]["snr"]
        map2 = np.array(map2).reshape(123, 123)

        # print(f"now workiong on {f1} and {f2}")

        new_map = map1 + map2
        new_dots = np.count_nonzero(new_map == 0)
        x, y = np.where(new_map == 0)
        pot=map1
        for hx in x:
            for hy in y:
                pot = new_map[hx - 1 : hx + 2, hy - 1 : hy + 2]
        # print(2 in pot)
        if 2 not in pot:
            # print(f"[-] handover: {new_t} rel: {(datetime.fromtimestamp(float(new_t))-datetime.fromtimestamp(float(last))).total_seconds()}")
            print(f" handover between {f1} and {f2}")
        else:
            print(f"no handover between {f1} and {f2}")
    # return suspected_handovers 

lista=detect_handovers("/home/rc/idp-castellotti/map-bw-stuff2")
print(lista)
