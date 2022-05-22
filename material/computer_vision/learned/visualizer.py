"""A dataset visualizer. Press ESC in the rendered window stop visualizing."""

import argparse

import cv2 as cv
from engine.configuration import load_config
from engine.datasets.factory import load_dataset
from engine.visualizer import Visualizable

ESCAPE_KEYCODE = 27


def main():
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("config", help="A pathname to a JSON config file")
    parser.add_argument(
        "validation",
        action="store_true",
        help="If set, visualize validation data. Else, training data.",
    )
    args = parser.parse_args()

    config = load_config(args.config)
    dataset = load_dataset(config, training=not args.validation)
    assert isinstance(
        dataset, Visualizable
    ), "Dataset must implement Visualizable."

    cv_win_name = "Dataset Visualizer"
    window = cv.namedWindow(cv_win_name, cv.WINDOW_NORMAL)  # Resizable.

    for index in range(len(dataset)):
        sample = dataset.get_visualizer_sample(index)
        print(sample.text)
        image = cv.cvtColor(sample.image, cv.COLOR_RGB2BGR)
        cv.imshow(cv_win_name, image)
        if cv.waitKey() == ESCAPE_KEYCODE:
            break


if __name__ == "__main__":
    main()
