# Dataset Visualization Implementation

## visualizer.py

The source for our visualizer tool looks as follows.

```py
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
```

Starting in `main`, we build our CLI. Different from `trainer.py`, we allow the
user to declare whether they want to visualize the training or validation split.
We then load our configuration and dataset. We require any dataset used with our
tool to implement the `Visualizable` interface. More on this later.

Next, we create an OpenCV
[named window](https://docs.opencv.org/4.x/d7/dfc/group__highgui.html#ga5afdf8410934fd099df85c75b2e0888b)
which we'll dispay our samples in.

Since we need to call our new method `get_visualizer_sample` on our datasets
instead of just invoking `__getitem__`, we have to loop over the length of our
dataset and call the new method explicitly. We print the dataset-provided text
and then render the image. We expect our image channels to be in RGB order, so
we
[convert the coloring](https://docs.opencv.org/4.x/d8/d01/group__imgproc__color__conversions.html)
to BGR for OpenCV's sake. Finally, if the user types `ESC` in the displayed
window, we stop iterating.

## engine/visualizer.py

Here is our new library code used by datasets that are compatible with our
visualizer tool.

```py
from typing import NamedTuple, Protocol, runtime_checkable

import numpy as np


class VisualizerSample(NamedTuple):
    """
    image: An image to visualize. It must be shaped as (H, W, C), RGB.
    text: Text to be printed.
    """

    image: np.ndarray
    text: str


@runtime_checkable
class Visualizable(Protocol):
    """The interface required by our engine's visualizer."""

    def get_visualizer_sample(index: int) -> VisualizerSample:
        """
        @p index An index into a dataset.
        @return A dataset sample prepared for use in the engine's visualizer.
        """
        raise NotImplementedError()
```

We create a new interface, called a
[`Protocol`](https://docs.python.org/3/library/typing.html#typing.Protocol) in
Python, and use
[`runtime_checkable`](https://docs.python.org/3/library/typing.html#typing.runtime_checkable)
to allow our visualizer tool to `assert isinstance(dataset, Visualizable)`,
which we showed earlier.

`Visualizable` returns a `VisualizerSample` which is another instance of an
annotated `typing.NamedTuple`. `VisualzerSample.image` is a `numpy.ndarray`
because OpenCV works with numpy arrays and not PyTorch tensors. Also, images in
numpy are often represented as `(H, W, C)`, where each letter is a shorthand for
height, width, and color channels respectively, so we require `image` to be in
that format.

## imagenette.py

Lastly, we extend `engine/imagenette.py` as follows.

```py
# ...

from engine.visualizer import Visualizable, VisualizerSample

# ...

class Imagenette(Sequence, Visualizable):

    # ...

    def get_visualizer_sample(self, index: int) -> VisualizerSample:
        """
        @p index An index into a dataset. Positive numbers must be less than
                 len(dataset).
        @return A dataset sample prepared for use in the engine's visualizer.
        """
        assert index < len(self), "Positive index out of range."

        sample = self[index]
        image = sample["inputs"].permute(1, 2, 0).numpy()
        text = f"index: {index}; class: {sample['targets']}"

        return VisualizerSample(image, text)
```

Here, we use
[`torch.permute`](https://pytorch.org/docs/stable/generated/torch.permute.html)
to reorder our image tensor. It was originally `(C, H, W)`, so we move the
channel dimension to the back. Then, we
[convert the tensor to a numpy array](https://pytorch.org/docs/stable/generated/torch.Tensor.numpy.html).
Lastly, we build `text`, an informational message to be printed with our sample.
It contains the sample index and the sample class.

## Running

When we run our tool, we see samples rendered and the following in the console.
Pressing any key except `ESC` advances the visualization to the next sample, and
`ESC` terminates visualization.

```
$ python3 visualizer.py configs/stub_config.json
index: 0; class: cassette_player
index: 1; class: cassette_player
<etc.>
```
