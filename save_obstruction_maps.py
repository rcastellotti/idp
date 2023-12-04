"""
save obstruction maps from get_obstruction_map endpoint 
"""
import os
import time
import argparse
import logging
import api

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
    obstruction_map = api.get_obstruction_map()
    os.makedirs(os.path.dirname(directory + "/"), exist_ok=True)
    with open(f"{directory}/map-{time.time()}.json", "w+", encoding="utf-8") as f:
        f.write(obstruction_map)
    time.sleep(0.5)
