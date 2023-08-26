import json
import os
import argparse
import ffmpeg
import matplotlib.pyplot as plt
import numpy as np
import logging

parser = argparse.ArgumentParser(prog="map")
parser.add_argument(
    "--verbose", "-v", help="verbose", action=argparse.BooleanOptionalAction
)
parser.add_argument("--directory", "-d", help="directory", required=True, type=str)
parser.add_argument("--output", "-o", help="output filename", required=True, type=str)

args = parser.parse_args()

directory = args.directory
os.makedirs(os.path.dirname(f"{directory}-viz/"), exist_ok=True)

if args.verbose:
    logging.basicConfig(level="INFO")


def process_file(filename):
    file = os.path.join(directory, filename)
    # print(img)
    with open(file, "r") as f:
        logging.info(f"elaborating {filename}")
        map = json.load(f)
        map = map["dishGetObstructionMap"]["snr"]
        map = np.array(map).reshape(123, 123)
        map = np.repeat(np.repeat(map, 2, axis=1), 2, axis=0)
        img = f"{directory}-viz/{filename}.png"
        print(img)
        plt.imshow(map, cmap="viridis")
        plt.axis("off")
        # burn = extract_between_dash_and_json(filename)
        # plt.text(
        #     map.shape[1] - 120,
        #     map.shape[0] - 10,  
        #     burn,
        #     color="yellow",
        #     fontsize=10,
        #     fontweight="bold",
        # )
        
        plt.savefig(img, bbox_inches="tight")
        plt.close()

files = os.listdir(directory)
for file in files:
    process_file(file)
print("All files processed.")

# ffmpeg.input(f"{directory}-viz/*.png", framerate=60, pattern_type="glob").output(
#     args.output,
#     vcodec="libx264",
#     pix_fmt="yuv420p",
#     vf="pad=ceil(iw/2)*2:ceil(ih/2)*2",
# ).run()
