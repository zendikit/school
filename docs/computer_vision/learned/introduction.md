# Learned Computer Vision

Learned computer vision differs from rule-based computer vision in that the
tuning of vision algorithms is done automatically by the machine instead of by
humans. In literature and elsewhere in this material, you will see machine-tuned
algorithms called "learned algorithms" although a human still typically outlines
the general algorithm. An algorithm for performing a computer vision task
subjected to learning is called a model, and a learned algorithm is called a
learned model or often also just "model."

The material here will have us build an engine to develop models and then the
models themselves. We'll do everything from scratch where reasonable. Examples
of things we consider unreasonable in this scope are reimplementing tensor
libraries and manually taking the gradient of our algorithms. Knowing how to do
both is valuable, but the former is an exercise in high-performance computing
and the latter becomes impractical as our algorithms grow in complexity.

## Prerequisites

This material is developed on a Linux-based machine with a modern, discrete
Nvidia GPU. You can use other operating systems, other types of GPUs, and
CPU-only machines, but our examples may not run directly on your environment.

For software, we'll do everything in Python 3, and our major dependencies will
include [`numpy`](https://numpy.org/), [`pytorch`](https://pytorch.org/), and
[`virtualenv`](https://virtualenv.pypa.io/en/latest/).

## Environment Setup

You can recreate the environment this material is created in via

```
git clone git@github.com:zendikit/school.git
cd wherever/you/want/your/code
pip3 install --user virtualenv
virtualenv --python python3.8 learned
cd learned
source ./bin/activate
ZENDIKIT_PATH=path_to_zendikit_school/material/computer_vision/learned
pip3 install -r $ZENDIKIT_PATH/requirements.txt
```
