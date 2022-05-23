# Dataset Visualization

With the current state of our engine and our imagenette dataset, if we want to
view a sample in Python, we are presented with the image as a tensor and the
class as a string name. The class name is clear to humans, but the
image-as-a-tensor is unfriendly when trying to understand what the image looks
like. For this purpose, it is helpful to implement a sample visualizer.

In our case, we'll build a visualizer that displays images from a dataset one
sample at a time. We'll do this in a new tool called `visualizer.py` that lives
next to `trainer.py`. We'll make `visualizer.py` dataset-agnostic similar to
`trainer.py`. To do this, our visualizer tool will expect that datasets
implement a method that takes a sample index and returns an image that can be
shown in an image viewer and a string that can be printed elsewhere, for example
in the console.

## Challenge

Implement a sample visualizer.

Hints:

There are a variety of Python packages that can display images. Examples are
[`PIL`](https://pillow.readthedocs.io/en/stable/),
[`matplotlib`](https://matplotlib.org/), and
[`OpenCV`](https://pypi.org/project/opencv-python/). We will use OpenCV because
it also provides mechanisms to wait for key presses from the user, allowing the
user to have more control over stepping through samples.

We will place library code in `engine/visualizer.py`.
