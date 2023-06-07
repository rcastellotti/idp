import time
from csv import writer
from datetime import datetime
import os
from starlink_grpc import status_data
from common import calculate_visible_satellites

# garching coordinates
observer_latitude = 48.2489
observer_longitude = 11.6532
observer_elevation = 0

file_exists = os.path.exists("visible_satellites.csv")

with open("visible_satellites.csv", "a+") as f:
    csv_writer = writer(f)
    if not file_exists:
        csv_writer.writerow(
            ["timestamp", "satellite_norad","satellite", "alt", "az", "pop_ping_latency_ms"]
        )

while True:
    with open("visible_satellites.csv", "a+") as f:
        csv_writer = writer(f)
        satellites = calculate_visible_satellites(
            observer_latitude, observer_longitude, observer_elevation
        )
        for sat, alt, az in satellites:
            pop_ping_latency_ms = status_data()[0]["pop_ping_latency_ms"]
            row=[datetime.now(), sat.model.satnum,sat.name, alt, az, pop_ping_latency_ms]
            csv_writer.writerow(row)
            print(row)  
    time.sleep(60)