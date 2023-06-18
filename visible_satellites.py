import time
from csv import writer
from datetime import datetime
import os
from starlink_grpc import status_data
from common import calculate_visible_satellites
import argparse
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import sessionmaker, declarative_base
from pprint import pprint


parser = argparse.ArgumentParser(prog="visible_satellites")
parser.add_argument(
    "--verbose", "-v", help="verbose", action=argparse.BooleanOptionalAction
)
parser.add_argument(
    "--latitude", "-lat", help="observer latitude", required=True, type=float
)
parser.add_argument(
    "--longitude", "-lon", help="observer longitude", required=True, type=float
)
parser.add_argument(
    "--elevation", "-el", help="observer evelation", required=True, type=float
)
parser.add_argument(
    "--distance", "-d", help="max distance for satellites (km)", required=True, type=int
)
# parser.add_argument("--output", "-o", help="output file", required=True)
args = parser.parse_args()

db_url = "sqlite:///satellites.db"
engine = create_engine(db_url)
Base = declarative_base()


class Satellite(Base):
    __tablename__ = "satellites"
    id = Column(Integer, primary_key=True)
    satname = Column(String)
    alt = Column(String)
    az = Column(String)
    start_timestamp = Column(String)
    end_timestamp = Column(String)
    visible = Column(Boolean, default=False, nullable=False)

    def __eq__(self, other):
        return self.satname == other.satname

    def __repr__(self):
        return f"Satellite {self.satname}"


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

while True:
    visible_satellites_db = (
        session.query(Satellite).filter(Satellite.visible.is_(True)).all()
    )
    start_time = datetime.now()
    vis_sat = calculate_visible_satellites(
        args.latitude, args.longitude, args.elevation, args.distance
    )
    visible_satellites = []
    for sat, alt, az in vis_sat:
        new_satellite = Satellite(
            satname=sat.name,
            alt=str(alt),
            az=str(az),
            start_timestamp=start_time,
            end_timestamp=start_time,
            visible=True,
        )
        visible_satellites.append(new_satellite)

    print("satellites visible now:")
    for s in visible_satellites:
        print(s)
    print("satellites that were visible last time:")
    for s in visible_satellites_db:
        print(s)

    for sat in visible_satellites_db:
        if sat in visible_satellites:
            sat.end_timestamp = start_time
            sat.visible=True
            visible_satellites.remove(sat)
        else:
            sat.visible = False
        session.add(sat)
        session.commit()
    # print(vis_sat)
    for s in visible_satellites:
        session.add(s)
        session.commit()
    
    time.sleep(5)