"""
visualize obstruction maps retrieved with `save_obstruction_maps`
"""

import json
import logging
import os
import argparse
import matplotlib.pyplot as plt
import numpy as np

parser = argparse.ArgumentParser(prog="map")
parser.add_argument(
    "--verbose", "-v", help="verbose", action=argparse.BooleanOptionalAction
)
parser.add_argument(
    "--input_directory", "-i", help="input directory", required=True, type=str
)
parser.add_argument(
    "--output_directory", "-o", help="output directory", required=True, type=str
)
args = parser.parse_args()

os.makedirs(args.output_directory, exist_ok=True)

if args.verbose:
    logging.basicConfig(level="INFO")


def process_file(filename, input_directory, output_directory):
    """
    process a single file from save_obstruction_maps
    """
    input_filename = os.path.join(input_directory, filename)
    with open(input_filename, "r", encoding="utf-8") as f:
        logging.info("elaborating %s", filename)
        obstruction_map = json.load(f)
        obstruction_map = obstruction_map["dishGetObstructionMap"]["snr"]
        obstruction_map = np.array(obstruction_map).reshape(123, 123)
        # augmenting the image
        obstruction_map = np.repeat(np.repeat(obstruction_map, 2, axis=1), 2, axis=0)
        img = f"{output_directory}/{filename}.png"
        plt.imshow(obstruction_map, cmap="viridis")
        plt.axis("off")
        plt.savefig(img, bbox_inches="tight")
        plt.close()


for file in os.listdir(args.input_directory):
    logging.info(file)
    process_file(file, args.input_directory, args.output_directory)
