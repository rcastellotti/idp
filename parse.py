# this data comes from
# bgpreader -w 1681562110,1681565710 -p ris -a 14593 is saved in `ris-dump-1h.txt`
# sample usage: python3 parse.py -i ris-dump-1h-a.txt -o ris-dump-1h-a.json
import csv
import argparse

csv.register_dialect("piper", delimiter="|", quoting=csv.QUOTE_NONE)

# <dump-type>|<elem-type>|<record-ts>|<project>|<collector>|<router-name>|<router-ip>|<peer-ASn>|<peer-IP>|<prefix>|<next-hop-IP>|<AS-path>|<origin-AS>|<communities>|<old-state>|<new-state>

from dataclasses import dataclass
from pygments import highlight, lexers, formatters
import json


class Record:
    def __init__(self, list):
        self.dump_type: str = list[0]
        self.elem_type = list[1]
        self.record_ts = list[2]
        self.project = list[3]
        self.collector = list[4]
        self.router_name = list[5]
        self.router_ip = list[6]
        self.peer_asn = list[7]
        self.peer_ip = list[8]
        self.prefix = list[9]
        self.next_hop_ip = list[10]
        self.as_path = list[11]
        self.origin_as = list[12]
        self.communities = list[13]
        self.old_state = list[14]
        self.new_state = list[14]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="parse", description="parse bgpreader outputs"
    )
    parser.add_argument("--input", "-i", help="input")
    parser.add_argument("--output", "-o", help="output file")
    args = parser.parse_args()
    dic = []
    with open(args.input, "r") as csvfile:
        for row in csv.reader(csvfile, dialect="piper"):
            read = Record(list=row)
            formatted_json = json.dumps(read.__dict__, indent=4)
            colorful_json = highlight(
                formatted_json, lexers.JsonLexer(), formatters.TerminalFormatter()
            )
            print(colorful_json)
            dic.append(read.__dict__)
    if args.output is not None:
        with open(args.output, "w") as outfile:
            json.dump(dic, outfile,indent=4)
