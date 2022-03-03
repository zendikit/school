"""
This script converts the Zendikit Japanese grammar represented as JSON into CSV.
"""

import argparse
import csv
import json
from pathlib import Path
from typing import Dict


# Map JLPT to numerical IDs such that if sorting in ascending order N5 comes first.
JLPT_TO_ID = {
  "n5": 0,
  "n4": 1,
  "n3": 2,
  "n2": 3,
  "n1": 4
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("json", help="The pathname to the Zendikit Japanese grammar JSON file.")
    parser.add_argument("--out", help="The filename to write output into; default is ./grammar.csv.")
    return parser.parse_args()


def main():
    args = parse_args()

    with open(args.json, "r") as f:
        grammar_json = json.load(f)

    # A base sort name is of the form (x)_(name) where `x` corresponds to the JLPT level (since we want to order N5
    # first, N5 corresponds to 0, N4 to 1, etc.), and `name` is the literal grammar point. Base sort names map to
    # the number of times the base name exists in a single JLPT level. By combining the base name and the number of
    # times `y`, we can build a unique "sort name" of the form (x)_(name)_(y).
    base_sort_names: Dict[str, int] = dict()

    out = Path(args.out) if args.out else Path("./grammar.csv")
    with open(out, "w", newline="") as f:
        csv_writer = csv.writer(f, quoting=csv.QUOTE_ALL)
        for point in grammar_json["points"]:
            # Get short names to most of the top-level data.
            level = point["level"]
            name = point["name"]
            meaning = point["meaning"]

            # Build the sort name. The sort name allows for ordering in tools like Anki.
            base_name = f"{JLPT_TO_ID[level]}_{name}"
            num_base_names = base_sort_names.get(base_name, 0)
            base_sort_names[base_name] = num_base_names + 1
            sort = f"{base_name}_{num_base_names}"

            # Now convert the list of example sentence pairs into a single (HTML) string.
            jp = '<div class="jp">'
            en = '<div class="en">'
            end = "</div>"
            example_sentences = "".join([f"{jp}{e['jp']}{end}{en}{e['en']}{end}" for e in point["example_sentences"]])

            csv_writer.writerow([sort, level, name, meaning, example_sentences])


if __name__ == "__main__":
    main()
