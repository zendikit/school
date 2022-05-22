from collections.abc import Sequence
from typing import Dict

from engine.datasets.imagenette import Imagenette


def load_dataset(config: Dict, training: bool) -> Sequence:
    """
    Load a dataset.

    @p config A configuration dictionary. The nested key `dataset.name` is
              required.
    @p training If True, load only training data; else only validation data.
    @return An instance of a loaded dataset.
    @exception ValueError `name` doesn't name a known dataset.
    """
    name = config["dataset"]["name"]

    if name == Imagenette.__name__:
        return Imagenette(config, training)

    raise ValueError(f"{name} doesn't name a known dataset")
