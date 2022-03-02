"""
This script converts the Zendikit Japanese grammar represented as JSON into CSV.
"""

import argparse
import csv
import json
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("json", help="The pathname to the Zendikit Japanese grammar JSON file.")
    parser.add_argument("--out", help="The filename to write output into; default is ./grammar.csv.")
    return parser.parse_args()


def main():
    args = parse_args()

    with open(args.json, "r") as f:
        grammar_json = json.load(f)

    out = Path(args.out) if args.out else Path("./grammar.csv")
    with open(out, "w", newline="") as f:
        csv_writer = csv.writer(f, quoting=csv.QUOTE_ALL)
        for i, point in enumerate(grammar_json["points"]):
            # Sort allows for ordering of points in tools such as Anki.
            sort = i

            # Get short names to most of the top-level data.
            level = point["level"]
            name = point["name"]
            meaning = point["meaning"]

            # Now convert the list of example sentence pairs into a single (HTML) string.
            jp = '<div class="jp">'
            en = '<div class="en">'
            end = "</div>"
            example_sentences = "".join([f"{jp}{e['jp']}{end}{en}{e['en']}{end}" for e in point["example_sentences"]])

            csv_writer.writerow([sort, level, name, meaning, example_sentences])


if __name__ == "__main__":
    main()
