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
        @p index An index into a dataset. Positive numbers must be less than
                 len(the_dataset).
        @return A dataset sample prepared for use in the engine's visualizer.
        """
        raise NotImplementedError()
