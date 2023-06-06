import time
import requests
from csv import writer
from datetime import datetime
import os
from starlink_grpc import status_data
import socket
from requests import adapters
from urllib3.poolmanager import PoolManager


class InterfaceAdapter(adapters.HTTPAdapter):
    def __init__(self, **kwargs):
        self.iface = kwargs.pop("iface", None)
        super(InterfaceAdapter, self).__init__(**kwargs)

    def _socket_options(self):
        if self.iface is None:
            return []
        else:
            return [(socket.SOL_SOCKET, socket.SO_BINDTODEVICE, self.iface)]

    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = PoolManager(
            num_pools=connections,
            maxsize=maxsize,
            block=block,
            socket_options=self._socket_options(),
        )


session = requests.Session()
for prefix in ("http://", "https://"):
    session.mount(prefix, InterfaceAdapter(iface=b"enp1s0f2"))

url = "https://releases.ubuntu.com/22.04.2/ubuntu-22.04.2-desktop-amd64.iso"
r = session.get(url, stream=True)
file_size = int(r.headers["content-length"])
print(f"file size: {file_size} bytes")
downloaded = 0
start = last_print = time.monotonic()
file_exists = os.path.exists("large_file_download.csv")

with open("large_file_download.csv", "a+") as f:
    csv_writer = writer(f)
    if not file_exists:
        csv_writer.writerow(["timestamp", "speed_KBs", "pop_ping_latency_ms"])

while True:
    r = session.get(url, stream=True)
    with open("large_file_download.csv", "a+") as f:
        csv_writer = writer(f)
        with open("ubuntu-22.04.2-desktop-amd64.iso.iso", "wb") as fp:
            for chunk in r.iter_content(chunk_size=4096):
                downloaded += fp.write(chunk)
                now = time.monotonic()
                if now - last_print > 1:
                    pct_done = round(downloaded / file_size * 100)
                    speed = downloaded / (now - start) /1024/1024
                    pop_ping_latency_ms = status_data()[0]["pop_ping_latency_ms"]
                    csv_writer.writerow([datetime.now(), speed, pop_ping_latency_ms])
                    print(f"Download {pct_done}% done, avg speed {speed} MBps")
                    last_print = now
    time.sleep(10)
