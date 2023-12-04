#!/usr/bin/python3
"""
simple CLI tool using `api`
"""
import argparse
import json
from pprint import pprint
import api

parser = argparse.ArgumentParser(prog="s(mol)tarlink cli")

parser.add_argument(
    "--obstruction_map",
    "-o",
    help="dish_get_obstruction_map",
    action=argparse.BooleanOptionalAction,
)
parser.add_argument(
    "--reboot", "-r", help="reboot", action=argparse.BooleanOptionalAction
)
parser.add_argument(
    "--status", "-s", help="status", action=argparse.BooleanOptionalAction
)

args = parser.parse_args()

if args.obstruction_map:
    pprint(json.loads(api.get_obstruction_map()))
elif args.reboot:
    pprint(json.loads(api.reboot()))
elif args.status:
    pprint(json.loads(api.get_status()))
else:
    parser.print_help()
