import csv
import json
from nine981 import get_status
from datetime import datetime
import argparse
import time

parser = argparse.ArgumentParser(prog="pop_ping_latency historic data")

parser.add_argument("--filename", "-f", help="filename", required=True)
parser.add_argument("--interval", "-i", help="interval", required=True, type=int)

args = parser.parse_args()

with open(args.filename, "a") as f:
    writer = csv.writer(f)
    writer.writerow(("timestamp", "pop_ping_latency_ms","downlinkThroughputBps"))

    while True:
        s = json.loads(get_status())
        lat=s["dishGetStatus"]["popPingLatencyMs"]
        bw=s["dishGetStatus"]["downlinkThroughputBps"]

        writer.writerow([datetime.now(), lat,bw])
        f.flush()
        time.sleep(args.interval)
