import os
import time
import argparse
import logging
import nine981

parser = argparse.ArgumentParser(prog="save obstruction maps")
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
if args.verbose:
    logging.basicConfig(level="INFO")

logging.info("starting to save maps")
for i in range(args.seconds):
    map = nine981.get_obstruction_map()
    os.makedirs(os.path.dirname(directory + "/"), exist_ok=True)
    with open(f"{directory}/map-{time.time()}.json", "w+") as f:
        f.write(map)
    time.sleep(0.5)
