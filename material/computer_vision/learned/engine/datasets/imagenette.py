"""Provides the imagenette2 dataset."""

import csv
import os
from collections.abc import Sequence
from typing import Dict, List, NamedTuple, Tuple

import torchvision
from PIL import Image

from engine.visualizer import Visualizable, VisualizerSample


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

        self._base_dir = os.path.dirname(csv_pathname)

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

        # Each tuple holds (path_to_image, image_class).
        self._data: List[_PathAndClass] = []
        self._to_tensor = torchvision.transforms.ToTensor()

        # Build the dataset index.
        with open(csv_pathname, "r") as f:
            # Indices into a row in the CSV file.
            img_path_idx = 0
            class_idx = 1
            valid_idx = 6

            reader = csv.reader(f)
            next(reader)  # Skip the first (header) row.

            for row in reader:
                is_valid = row[valid_idx] == "True"
                # Skip samples that don't match our dataset type (train/valid).
                if training and is_valid or not training and not is_valid:
                    continue

                img_path = os.path.join(self._base_dir, row[img_path_idx])
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
