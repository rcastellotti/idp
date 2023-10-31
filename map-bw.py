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


def get_obstruction_maps():
    print("starting to save maps")
    for i in range(args.seconds):
        map = nine981.get_obstruction_map()
        os.makedirs(os.path.dirname(directory + "/"), exist_ok=True)
        with open(f"{directory}/{int(time.time())}.json", "w+") as f:
            f.write(map)
        time.sleep(1)
    os.exit(0)


def function2():
    common.measure_bw(directory + ".csv")


def function3():
    subprocess.run(
        [
            "curl",
            "--interface",
            "enp1s0f3",
            "http://ftp.uio.no/debian-cd/12.1.0-live/amd64/iso-hybrid/debian-live-12.1.0-amd64-lxde.iso",
            "--output",
            "/dev/null",
        ]
    )


if __name__ == "__main__":
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future1 = executor.submit(get_obstruction_maps)
        future2 = executor.submit(function2)
        future3 = executor.submit(function3)
        concurrent.futures.wait([future1, future2, future3])
