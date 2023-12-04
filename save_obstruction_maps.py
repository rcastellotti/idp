"""
save obstruction maps from get_obstruction_map endpoint, remember to reboot (./s.py -r)
Sample usage:
python3 save_obstruction_maps -i 500 -o ./obstruction_maps
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
parser.add_argument("--output", "-o", help="output_directory", required=True, type=str)
parser.add_argument(
    "--interval",
    "-interval",
    help="how many seconds we should collect maps for",
    required=True,
    type=int,
)


def main(directory, interval):
    """
    save obstruction maps into directory
    """
    logging.info("starting to save maps")
    for _ in range(interval):
        obstruction_map = api.get_obstruction_map()
        os.makedirs(os.path.dirname(directory + "/"), exist_ok=True)
        with open(f"{directory}/map-{time.time()}.json", "w+", encoding="utf-8") as f:
            f.write(obstruction_map)
        time.sleep(0.5)


if __name__ == "__main__":
    args = parser.parse_args()
    if args.verbose:
        logging.basicConfig(level="INFO")
    main(args.output, args.interval)
