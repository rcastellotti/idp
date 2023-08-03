import concurrent.futures
import os
import time
import argparse
import common
import nine981
import subprocess

parser = argparse.ArgumentParser(prog="map")
parser.add_argument(
    "--verbose", "-v", help="verbose", action=argparse.BooleanOptionalAction
)
parser.add_argument("--directory", "-d", help="directory", required=True, type=str)
parser.add_argument(
    "--seconds",
    "-s",
    help="how many seconds we should collect maps for",
    required=True,
    type=int,
)
args = parser.parse_args()

directory = args.directory


def function1():
    print("starting to save maps")
    for i in range(args.seconds):
        map = nine981.get_obstruction_map()
        os.makedirs(os.path.dirname(directory + "/"), exist_ok=True)
        with open(f"{directory}/map-{int(time.time())}.json", "w+") as f:
            f.write(map)
        time.sleep(1)
    os.exit(0)


def function2():
    common.measure_bw("bw.csv")


def function3():
    subprocess.run(
        [
            "wget",
            "-4",
            "http://ftp.uio.no/debian-cd/12.1.0-live/amd64/iso-hybrid/debian-live-12.1.0-amd64-lxde.iso",
            "--bind-address",
            "192.168.1.0",
            "-O",
            "/dev/null",
        ]
    )


urls = [
    "http://mirror.de.leaseweb.net/debian-cd/12.1.0-live/amd64/iso-hybrid/debian-live-12.1.0-amd64-lxde.iso",
    "http://mirror.nl.datapacket.com/debian-cd/12.1.0-live/amd64/iso-hybrid/debian-live-12.1.0-amd64-lxde.iso",
    "http://ftp.uio.no/debian-cd/12.1.0-live/amd64/iso-hybrid/debian-live-12.1.0-amd64-lxde.iso",
]

if __name__ == "__main__":
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future1 = executor.submit(function1)
        future2 = executor.submit(function2)
        future3 = executor.submit(function3)
        concurrent.futures.wait([future1, future2, future3])
