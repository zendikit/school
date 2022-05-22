# Dataset Implementation

## trainer.py

Below are our changes to our trainer.

```py
# ...

from engine.configuration import load_config
from engine.datasets.factory import load_dataset
from engine.models import build_model


def main():
    # ...

    config = load_config(args.config)
    training_dataset = load_dataset(config, training=True)
    validation_dataset = load_dataset(config, training=False)
    model = build_model()

    # ...
```

We now import `load_dataset` from `engine.datasets.factory.py`. Also, we
instantiate both a `training_dataset` and `validation_dataset`. We pass the
`config` into `load_dataset` since the configuration contains not only the name
of the dataset we want to load but also additional values the dataset instance
itself will need. `load_dataset` also features a `training` parameter that we
use to indicate whether we want to load training data or validation data.

## factory.py

`factory.py` looks as follows.

```py
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
```

In the documentation, we declare the required keys in the configuration. This
practice is important because `config` is otherwise opaque--we don't know which
keys and values it has, and our users won't know which we require unless we
document our expectations.

`load_dataset` expects that all datasets implement the
`collections.abc.Sequence` interface, so we have `load_dataset` declare that it
simply returns something you can iterate over. Also, we compare
`name == Imagenette.__name__` instead of comparing `name == "Imagenette"`
because, were someone to refactor `Imagenette` and change its name, the
condition here will always check against the class name proper and not a
potentially out-of-date string.

## stub_config.json

Our configuration now looks as follows.

```json
{
  "dataset": {
    "name": "Imagenette",
    "path": "/abs/path/to/imagenette2/noisy_imagenette.csv"
  },
  "trainer": {
    "num_iters": 1
  }
}
```

We add a new `dataset` object that contains the name of the dataset, which we
choose to match the name of the class we implemented, and a path to a file
describing the dataset.

## imagenette.py

Lastly, here is our implementation of `engine/datasets/imagenette.py`.

```py
"""Provides the imagenette2 dataset."""

import csv
import os
from collections.abc import Sequence
from typing import Dict, List, NamedTuple, Tuple

import torchvision
from PIL import Image


class _PathAndClass(NamedTuple):
    path: str
    cls: str


class Imagenette(Sequence, Visualizable):
    def __init__(self, config: Dict, training: bool):
        """
        @p config A configuration dictionary. The nested key `dataset.path` is
                   required. `dataset.path` is assumed to point to
                   noisy_imagenette.csv.
        @p training If True, load only training data; else only validation data.
        """
        csv_pathname = config["dataset"]["path"]

        self._class_remapper = {
            "n01440764": "tench",
            "n02102040": "english_springer",
            "n02979186": "cassette_player",
            "n03000684": "chainsaw",
            "n03028079": "church",
            "n03394916": "french_horn",
            "n03417042": "garbage_truck",
            "n03425413": "gas_pump",
            "n03445777": "golf_ball",
            "n03888257": "parachute",
        }

        self._data: List[_PathAndClass] = []
        self._to_tensor = torchvision.transforms.ToTensor()

        # Build the dataset index.
        with open(csv_pathname, "r") as f:
            # Indices into a row in the CSV file.
            img_path_idx = 0
            class_idx = 1
            valid_idx = 6

            base_dir = os.path.dirname(csv_pathname)

            reader = csv.reader(f)
            next(reader)  # Skip the first (header) row.

            for row in reader:
                is_valid = row[valid_idx] == "True"
                # Skip samples that don't match our dataset type (train/valid).
                if training and is_valid or not training and not is_valid:
                    continue

                img_path = os.path.join(base_dir, row[img_path_idx])
                img_class = row[class_idx]
                self._data.append(_PathAndClass(img_path, img_class))

    def __len__(self) -> int:
        """@return The number of samples in the dataset."""
        return len(self._data)

    def __getitem__(self, index: int) -> Dict:
        """
        @p index An index into the dataset. Positive numbers must be less than
                 len(dataset).
        @return A dictionary with:
                "inputs": A torch.Tensor containing the image as (C, H, W).
                "targets": The class of the object in the `inputs` tensor.
        """
        assert index < len(self), "Positive index out of range."

        with Image.open(self._data[index].path) as img:
            img_tensor = self._to_tensor(img)

        return {
            "inputs": img_tensor,
            "targets": self._class_remapper[self._data[index].cls],
        }
```

Let's jump right to the `Imagenette` implementation.

As with `load_dataset`, we document our key and value expectations for `config`.

We provide our class name remapper as `self._class_remapper`. Next, we
initialize our dataset index as `self._data`.

`self._data` is a list of `_PathAndClass` instances. `_PathAndClass` serves only
to hold a path to an image and the class of the image in our context, and it
derives from `typing.NamedTuple` to allow us to annotate the field names. We
could use a plain tuple, but we would then be lacking the self-documenting
property of a named tuple.

Next we instantiate a
[`torchvision.transforms.ToTensor`](https://pytorch.org/vision/main/generated/torchvision.transforms.ToTensor.html).
We'll discuss this more later.

Finally in `__init__`, we iterate through the CSV file's rows and build our
dataset index.

`__len__` is self-explanatory.

`__getitem__` uses
[`Pillow.Image`](https://pillow.readthedocs.io/en/stable/reference/Image.html)
to load an image from disk. We then use our aforementioned `self._to_tensor`
Torchvision transformation to convert the Pillow image to a Torch tensor.
Finally, we build the dictionary to return but remap the sample's class name
before adding it to the dictionary.

## Testing

We could imagine adding a test for `Imagenette`. The test might confirm the
number of training and validation samples loaded, check that the first and last
sample of each dataset matches what is specified in `noisy_imagenette.csv`, and
also fetch a sample out of the datasets and confirm the returned dictionary's
keys and values.

This all relies on the data being available, though, which is not a big problem
for us right now but quickly becomes a problem when developing an engine at
scale, where we have an arbitrary number of developers contributing to the
source code. We can't anticipate where each dataset we might need for tests
lives on disk in the runtime without the user doing so manual work to specify
it. Also, if the datasets are massive, it's unfriendly to require other
developers to have to download them to run the tests.

If we run our tests in a consistent, standardized environment, though, such as
containerized as part of some continuous integration, then these tests become
more feasible. An alternative is to create a very small subset of a large
dataset and use this in testing. Locating this on an end-user's system reliably
could be done by having the engine itself fetch the dataset from some networked
server, for example.

In our case here, we'll do a manual test only. For example, we can use
[the Python debugger](https://docs.python.org/3/library/pdb.html) and break
somewhere in `trainer.py`.

```py
config = load_config(args.config)
training_dataset = load_dataset(config, training=True)
validation_dataset = load_dataset(config, training=False)
breakpoint()  # Stop here.
model = build_model()
```

We could then inspect the datasets in the debugger.

```
(Pdb) p len(training_dataset)
9469
(Pdb) p len(validation_dataset)
3925
(Pdb) p training_dataset[0]
{'inputs': tensor(  # ...
         ), 'targets': 'cassette_player'}
(Pdb) p training_dataset[-1]
{'inputs': tensor(  # ...
         ), 'targets': 'gas_pump'}
```
