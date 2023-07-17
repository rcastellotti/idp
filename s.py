#!/usr/bin/python3

import argparse
import nine981
import json
from pprint import pprint
parser = argparse.ArgumentParser(prog="s(mol)tarlink cli")

parser.add_argument("--obstruction_map", "-o", help="dish_get_obstruction_map", action=argparse.BooleanOptionalAction)
parser.add_argument("--reboot", "-r", help="reboot", action=argparse.BooleanOptionalAction)
parser.add_argument("--status", "-s", help="status", action=argparse.BooleanOptionalAction)

args = parser.parse_args()

if args.obstruction_map:
    pprint(json.loads(nine981.get_obstruction_map()))
elif args.reboot:
    pprint(json.loads(nine981.reboot()))
elif args.status:
    pprint(json.loads(nine981.get_status()))
else:
    parser.print_help()
