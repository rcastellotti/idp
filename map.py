import json
import os
import time
import argparse
import ffmpeg
import matplotlib.pyplot as plt
import numpy as np
import logging
import nine981
from PIL import Image, ImageDraw,ImageFont

parser = argparse.ArgumentParser(prog="map")
parser.add_argument(
    "--verbose", "-v", help="verbose", action=argparse.BooleanOptionalAction
)
parser.add_argument(
        "--directory", "-d", help="directory", required=True, type=str
)
parser.add_argument(
        "--output", "-o", help="output filename", required=True, type=str
)
parser.add_argument(
        "--seconds","-s", help="how many seconds we should collect maps for", required=True, type=int
)
args = parser.parse_args()

directory=args.directory
if args.verbose:
    logging.basicConfig(level="INFO")

# logging.info("starting to save maps")
# for i in range(1):
#     map = nine981.get_obstruction_map()
#     os.makedirs(os.path.dirname(directory + "/"), exist_ok=True)
#     with open(f"{directory}/map-{int(time.time())}.json", "w+") as f:
#         f.write(map)
#     time.sleep(1)

for file in os.listdir(directory):
    with open(f"{directory}/{file}", "r") as f:
        logging.info(f"elaborating {file}")
        map = json.load(f)
        map = map["dishGetObstructionMap"]["snr"]
        map = np.array(map).reshape(123, 123)
        map = np.repeat(np.repeat(map, 10, axis=1), 10, axis=0)
        plt.imshow(map)
        os.makedirs(os.path.dirname(f"{directory}-viz/"), exist_ok=True)
        img=f"{directory}-viz/{file}.png"
        plt.axis("off")
        plt.savefig(img)
        image=Image.open(img)
        W, H = image.size
        # font = ImageFont.truetype("/usr/share/fonts/truetype/noto/NotoSansMono-Bold.ttf", 15)
        font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Unicode.ttf", 15)
        draw = ImageDraw.Draw(image)
        _, _, w, h = draw.textbbox((0, 0), img)
        draw.text(((W - w) / 2, (H - h)-150), img, font=font,fill="yellow")
        image.save(img)

ffmpeg.input( f"{directory}-viz/*.png", framerate=30, pattern_type="glob").output(
    args.output,
    vcodec="libx264",
    pix_fmt="yuv420p",
    vf="pad=ceil(iw/2)*2:ceil(ih/2)*2",
).run()

# we can "sum" the matrices to see how many times we saw a satellite in a certain pixel, that will result in pixel
# with darker colors and we can visualize it better
