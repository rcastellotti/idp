from common import detect_handovers
import argparse

parser = argparse.ArgumentParser(prog="hand")

parser.add_argument(
    "--verbose", "-v", help="verbose", action=argparse.BooleanOptionalAction
)
parser.add_argument("--directory", "-d", help="directory", required=True, type=str)

args = parser.parse_args()
detect_handovers(args.directory)