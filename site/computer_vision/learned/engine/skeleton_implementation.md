# Skeleton Implementation

Here is how we implemented our skeleton. The source tree is

```
configs
└── stub_config.json
engine
├── configuration.py
├── datasets.py
├── __init__.py
└── models.py
trainer.py
```

## trainer.py

```py
"""A model trainer."""

import argparse

from engine.configuration import load_config
from engine.datasets import load_dataset
from engine.models import build_model

def main():
    parser = argparse.ArgumentParser(
            description=__doc__,
            formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("config", help="A pathname to a JSON config file")
    args = parser.parse_args()

    config = load_config(args.config)
    dataset = load_dataset()
    model = build_model()

    # Training loop.
    for iteration in range(config["trainer"]["num_iters"]):
        pass

if __name__ == "__main__":
    main()
```

We start by importing our configuration and dataset factories from their respective modules. We also anticipate some kind of model
factory, so we import that as well.

We use `argparse` to build the command-line interface. Our interface takes a single, required argument, a pathname to a JSON
configuration file. We also make the file's docstring part of the command-line help text.

Next we load our `config` and then the placeholders for our `dataset` and `model`.

Then, we enter the training loop. Our condition, the maximum number of iterations, is taken directly from the user-provided
configuration. We don't have anything to do inside the training loop yet, so we `pass`.

## configuration.py

We implement our configuration loader as follows.

```py
import json
from typing import Dict

def load_config(config_pathname: str) -> Dict:
    """
    Load a configuration from a JSON file on disk.

    @p config_pathname A pathname to a JSON file to load.
    @return The loaded configuration.
    """
    with open(config_pathname, "r") as f:
        return json.load(f)
```

For our documentation, we choose the [Doxygen style](https://www.doxygen.nl/manual/docblocks.html).

We let `open` handle reporting issues with `config_pathname` such as file-not-found or not-a-regular-file errors.

## datasets.py

Our dataset factory looks as follows.

```py
def load_dataset() -> None:
    """@return None"""
    # Currently unimplemented.
    return None
```

We have nothing to do here yet, so we simply return `None`. An alternative is raising `NotImplementedError`, but `None` allows us to
run `trainer.py` from start to finish.

## models.py

Our model factory looks very similar to our dataset one at this time.

## stub\_config.json

Our configuration looks like

```json
{
  "trainer": {
    "num_iters": 1
  }
}
```

The value is arbitrary at this time.

## Running trainer.py

You should be able to run `trainer.py` without errors in your implementation, unless you chose to raise `NotImplementedError`s in your
stubs.
