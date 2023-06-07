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

file_exists = os.path.exists("visible_satellites_variable_distance.csv")

with open("visible_satellites_variable_distance.csv", "a+") as f:
    csv_writer = writer(f)
    if not file_exists:
        csv_writer.writerow(
            [
                "timestamp",
                "distance",
                "satellite_norad",
                "satellite",
                "alt",
                "az",
                "pop_ping_latency_ms",
            ]
        )

distance=0

while True:
    if distance==3000:
        break
    with open("visible_satellites_variable_distance.csv", "a+") as f:
        csv_writer = writer(f)
        
        satellites = calculate_visible_satellites(
            observer_latitude, observer_longitude, observer_elevation, distance_km=distance
        )
        for sat, alt, az in satellites:
            pop_ping_latency_ms = status_data()[0]["pop_ping_latency_ms"]
            row = [
                datetime.now(),
                distance,
                sat.model.satnum,
                sat.name,
                alt,
                az,
                pop_ping_latency_ms,
            ]
            csv_writer.writerow(row)
            print(row)
    distance+=100
