"""
save satellite appearance patterns to a sqlite database
`scratch`.ipynb contains a cell to visualize the data created
by this script.
Sample usage:
python3 patterns_in_satellite_appearances.py -v -lat 48.2489 -lon 11.6532 -el 0 -d 800
"""
import time
import logging
import argparse
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base
from common import calculate_visible_satellites

parser = argparse.ArgumentParser(
    prog="retrieve visible satellites (you get to define what visible means)"
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
parser.add_argument(
    "--verbose", "-v", help="verbose", action=argparse.BooleanOptionalAction
)

DB_URL = "sqlite:///satellites.sqlite"
engine = create_engine(DB_URL)
Base = declarative_base()


class Satellite(Base):
    """
    satellite class, needed by SQLAlchemy
    """

    __tablename__ = "satellites"
    id = Column(Integer, primary_key=True)
    relative_ts = Column(Integer)
    ts = Column(Integer)
    satname = Column(String)
    alt = Column(String)
    az = Column(String)

    def __eq__(self, other):
        return self.satname == other.satname

    def __repr__(self):
        return f"Satellite {self.satname}"


def main(latitude, longitude, elevation, distance):
    """
    Retrieve visible satellites
    """
    Base.metadata.create_all(engine)
    session = sessionmaker(bind=engine)()
    count = 0
    while True:
        count += 1
        timestamp = time.time()
        vis_sat = calculate_visible_satellites(latitude, longitude, elevation, distance)
        for sat, alt, az in vis_sat:
            new_satellite = Satellite(
                satname=sat.name,
                relative_ts=count,
                alt=str(alt),
                az=str(az),
                ts=timestamp,
            )
            logging.info(sat)
            session.add(new_satellite)
            session.commit()
        time.sleep(15)


if __name__ == "__main__":
    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(level="INFO")
    main(args.latitude, args.longitude, args.elevation, args.distance)
