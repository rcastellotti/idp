import os
import json
import numpy as np
dir="./raw_maps_to_analyz"
count=0
for f in sorted(os.listdir(dir)):
    count+=1
    if count==10:
        break
    fv=os.path.join(dir+"-viz",f)+".png"
    f=os.path.join(dir,f)
    map = json.load(open(f))
    map = map["dishGetObstructionMap"]["snr"]
    map = np.array(map).reshape(123, 123)
    # print(map)
    print(f)
    print(fv)

    is_present = np.any(map == 1)
    if (is_present):
        x,y=np.where(map == 1)
        x=x[0]
        y=y[0]
        print(f"\n\t{x,y}\n")
        pot = map[x - 1:x + 2, y - 1:y + 2]
        print(pot)
    # break




    # this assumes each time we only have a new value
    # map = np.array([
#  [-1, -1, -1, -1, -1],
#  [-1, 1, -1, -1, -1],
#  [-1, -1, -1, -1, -1],
#  [-1, -1, -1, -1, -1],
#  [-1, -1, -1, -1, -1]]
# )

# map2 = np.array([
#  [-1, -1, -1, -1, -1],
#  [-1, 1, -1, -1, -1],
#  [-1, -1, 1, -1, -1],
#  [-1, -1, -1, -1, -1],
#  [-1, -1, -1, -1, -1]]
# )

# print(map+map2)


# by summing matrices we can detect the new