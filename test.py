import time
from tqdm import tqdm
import requests


def download_file(url):
    local_filename = url.split("/")[-1]
    # using these headers because I had some problems downloading this specific file without them
    headers = {
        "User-Agent": "Wget/1.21.4",
        "Accept": "*/*",
        "Accept-Encoding": "identity",
        "Connection": "Keep-Alive",
    }

    with requests.get(url, stream=True, headers=headers) as r:
        start_time = time.time()
        r.raise_for_status()
        with open(local_filename, "wb") as f:
            for chunk in r.iter_content(chunk_size=1024):
                f.write(chunk)
                elapsed_time = time.time() - start_time
                download_speed_kbs = len(chunk) / elapsed_time / 1024
                print(f"Download speed: {download_speed_kbs:.2f} KB/s", end="\r")
                f.write(chunk)
    return local_filename


url = "http://speed.hetzner.de/10GB.bin"

download_file(url)
