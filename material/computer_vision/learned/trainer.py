"""A model trainer."""

import argparse

from engine.configuration import load_config
from engine.datasets.factory import load_dataset
from engine.models import build_model


def main():
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("config", help="A pathname to a JSON config file")
    args = parser.parse_args()

    config = load_config(args.config)
    training_dataset = load_dataset(config, training=True)
    validation_dataset = load_dataset(config, training=False)
    model = build_model()

    # Training loop.
    for iteration in range(config["trainer"]["num_iters"]):
        pass


if __name__ == "__main__":
    main()
