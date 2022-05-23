# Datasets

Just as with deep learning in general, at the core of training a model for
computer vision tasks is lots of data. The tunable parts of our models are
called parameters. Parameters are simply numerical values in tensors that
participate in the math done in the algorithm.

In rule-based algorithms, humans tune the algorithms based on intuition (the
side of a car has a shape that looks like _this_ and the front a shape that
looks like _that_) and small-scale feedback loops (we found we can identify cars
with their doors closed, but we forgot about cars with their doors open, so we
need to add a case for those). The fundamental parts that something like a car
is decomposed into in an image are called features. In rule-based algorithms,
features are hand-selected and hand-tuned.

Imaging trying to come up with a list of criteria for what constitutes a car.
Now image a car that somehow is not captured by those criteria. If you think
you've found a list of criteria that describes a majority of cars, now consider
how you'd code that criteria. This has proven to be impractical for humans.

In learned computer vision, the machine not only tunes the algorithm but also
discovers the features. These features are hardly intuitive to humans; for now
it's sufficient to say (going with the car example) that they are mathematical
relationships between some weighted combination of every instance of a car that
our model has seen in training. If we are training our model from scratch, then
before the first iteration, it has never "seen" a car before, unlike a human who
has likely seen cars everyday for years if not decades. In order for our model
to generalize well, we need to show it very many cars.

This is where the _dataset_ comes into play. A dataset in our context is a
collection of training data and annotations. Following our example of cars, the
training data could be images with (and without!) cars in them. We would provide
these to our model and "ask" it to identify all cars in some image. The
annotations (or _ground truth_, or _targets_) are metadata about each image. The
metadata might contain information such as the regions of an image occupied by
cars. We compare what the annotations say about an image with what our model
says about the same image to determine how well our model performed its _tasks_
on that image. Things such as classification (_what_ is this an image of--a car,
a person, a tree?), detection (_where_ are the cars in this image?), and
segmentation (does this pixel belong to a car, a road, a tree, or maybe
something else?) are examples of tasks.

Datasets are typically created around certain subject matter and for specific
tasks. For example, the [CIFAR-10](https://www.cs.toronto.edu/~kriz/cifar.html)
dataset features 10 classes of objects (animals, boats, vehicles) with 6,000
images per class. [MNIST](http://yann.lecun.com/exdb/mnist/) contains 70,000
images of hand-written digits 0-9. [ImageNet](https://image-net.org/index)
contains 1000 classes of general objects and over 1 million training images. The
[Waymo Open Dataset](https://waymo.com/open/) is focused on autonomous driving
and contains _scenes_ (consecutive images taken while driving, essentially
video) of autonomous driving captured by multiple sensors (cameras,
[Lidar](https://en.wikipedia.org/wiki/Lidar)) with annotations for detection and
segmentation of vehicles, pedestrians, roads, etc. The featurefulness of this
dataset is updated over time.

As suggested before, to generalize well, we need lots of data. That, coupled
with the representation of the data (for example, possibly very large images)
makes some datasets very large. MNIST is approximately 10 MB, CIFAR-10 about 160
MB, ImageNet is about 150 GB, and the Waymo Open Dataset is over 300 GB.

## Our First Dataset

Our first dataset will be [imagenette](https://github.com/fastai/imagenette), a
subset of the ImageNet dataset. Imagenette contains only 10 classes. We'll use
the version containing full-size images which is 1.5 GB, compressed. If you'd
like to follow along, download that dataset now. The latest commit at the time
of our download was
[6d5d92e](https://github.com/fastai/imagenette/commit/6d5d92efc959918fcdb90e149e20d3198dfa34a8).
When extracted, you'll see the following directory structure:

```
imagenette2
├── noisy_imagenette.csv
├── train
│   ├── n01440764
│   │   ├── ILSVRC2012_val_00000293.JPEG
│   │   └── ...
│   └── ...
└── val
    ├── n01440764
    └── ...
```

`noisy_imagenette.csv` contains the dataset annotations and associates each
annotation with a single JPEG image. The dataset README explains the meaning of
the CSV header, but we'll clarify some details here. First, values such as
`n01440764` are class names. All images of class `n01440764` are stored in
folder `n01440764`. Second, the full form of the `is_valid` header field is
`is_validation`. `val` in the file tree also indicates `validation`. To
understand this, we need to briefly discuss dataset _splits_.

## Dataset Splits

So far, we've discussed data used for _training_ our model, but how do we
benchmark our model to see how well it performs its tasks? We **cannot** use our
training data. The model may have _memorized_ any image it has already seen from
the training dataset. Here, memorized means that the model encodes information
about a specific input it has seen that allows it to perform its tasks on that
particular input very well, if not perfectly. In other words, the model may have
a bias toward that input, and its performance on that input is not
representative of its general performance.

We need to keep the data we use for validation (or _testing_, _evaluation_,
_benchmarking_, etc.) separate from the data we use for training. One way to do
this is with a _train/validation split_. In the case of imagenette, that split
is 70/30 at the time of this writing, meaning that 70% of the data is provided
for training and 30% is reserved for validation. The validation data lives in
the `val` folder in imagenette and is marked with `True` in the `is_valid`
column of `noisy_imagenette.csv`.

When it comes time to test the model's performance, we put the model into a mode
that prevents it from learning and then run some data from the validation split
through the model. This way, we test the model with data is has never seen
before, and we prevent it from adjusting its tuning based on the data we just
showed it.

## Engine Interface

We've discussed the dataset as it lives on disk. Now, let's briefly cover how we
interface with the dataset in Python. Because datasets can be very large, much
larger than available system RAM, a common practice is to build an _index_ of
the data on disk at runtime. That is, we don't load all of the data into RAM at
once. Rather, we learn where the data lives on disk and load only what we need
on-demand.

At runtime, we learn about the dataset typically by loading one or more files
describing the dataset. In the case of imagenette, we only need to parse a
single file, `noisy_imagenette.csv`.

As a dataset is just a collection of items, let's have ours implement the Python
object model's
[`sequence` interface](https://docs.python.org/3/glossary.html#term-sequence).
This way our users can fetch samples from our dataset conveniently, such as by

```py
# Get the ith sample.
the_dataset[i]

# Iterate through the dataset.
for sample in the_dataset:
    ...
# Alternatively:
iter(the_dataset)

# Get the total number of samples in the dataset.
len(the_dataset)
```

What does `the_dataset[i]` return, though? The examples of datasets listed above
are enough to demonstrate that there is no shared interface between data from
different datasets. However, each dataset in the examples above do provide the
same thing conceptually: data to be input to a model and annotations containing
the ground truth corresponding to the model input. `the_dataset[i]` can thus
return a dictionary containing

```py
{
    "inputs": loaded_images,
    "targets": loaded_annotations,
}
```

The type of `loaded_images` and `loaded_annotations` depends on the dataset. For
computer vision, `loaded_images` will typically be one or more images stored as
tensors in a list or dictionary, or the images might be batched into a single
tensor. `loaded_annotations` is often a dictionary. We'll cover these
representations in more detail in later material.

For now, for imagenette, let's use the following interface

```py
{
    "inputs": torch.Tensor, # An image loaded from disk.
    "targets": str, # The class name corresponding to the loaded image.
}
```

We'll need to change this interface when we develop our first model, but we
don't understand why yet, so we will return to this later.

## Challenge

Implement an imagenette dataset for our engine. So far, we've used the term
"dataset" to describe an archive we downloaded and stored on disk; however,
we'll also call whatever instance we create at runtime to get at the data on
disk a dataset.

In particular:

1. Extend our single JSON configuration file to specify the dataset to load.
1. Extend our dataset factory to create an instance of the requested dataset.
1. Have your dataset implement Python's
   [`sequence` interface](https://docs.python.org/3/glossary.html#term-sequence).
1. Have your dataset return samples conforming to our interface in _Engine
   Interface_.

Hints:

There are many ways to load an image from disk and store it as a Torch tensor.
If you're using the environment this material is created in, we already have
access to `numpy`, `torch`, `torchvision`, and `PIL`
([`pillow`](https://pillow.readthedocs.io/en/stable/)). No one of these things
can load from disk directly to a Torch tensor by itself.

For imagenette, class names such as `n01440764` are not very human-friendly. You
can find a friendlier mapping
[here](https://docs.fast.ai/tutorial.imagenette.html).

We will change `engine/datasets.py` into a directory, `engine/datasets/`, so
that we can store our dataset implementations in their own files.

Lastly, we will instantiate two datasets, one for training data and one for
validation data.
