from threading import Thread
from time import sleep
import subprocess
import logging
import argparse
from common import cloud_traceroutes
import time
parser = argparse.ArgumentParser(prog="traceroute")

parser.add_argument(
    "--verbose", "-v", help="verbose", action=argparse.BooleanOptionalAction
)

# parser.add_argument("--directory", "-d", help="where to store files", required=True)
# parser.add_argument("--asndb", "-a", help="asndb file location", required=True)
# parser.add_argument("--region_file", "-r", help="region file  (csv)", required=True)

args = parser.parse_args()
if args.verbose:
    logging.getLogger().setLevel(logging.DEBUG)
    logging.getLogger("urllib3").setLevel(logging.WARNING)

else:
    logging.getLogger().setLevel(logging.INFO)

# run for 12 hours while also running iperf
args.asndb="/home/rc/idp-castellotti-data/ipasn_20230315.dat"
args.region_file="/home/rc/idp-castellotti/targets.csv"
args.directory="/home/rc/idp-castellotti-data/traceroutes-iperf-5bks"

duration=60*60*12
start_time = time.time()
end_time = start_time + duration

print(end_time)
def tr():
    while time.time() < end_time:
        cloud_traceroutes(args.region_file,args.directory,args.asndb)
        time.sleep(1)

def iperf():
    while time.time() < end_time:
        subprocess.run(["iperf" ,"-c", "138.246.253.20", "-p 5001", "-u" ,"-b 5k"])

if __name__ == "__main__":
    thread1 = Thread(target = tr)
    thread2 = Thread(target = iperf)
    thread1.start()
    thread2.start()
    thread2.join()
    thread1.join()