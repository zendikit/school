# Engine Skeleton

The "engine" is what we'll call the software that facilitates "training."

## Training

"Training" is the process of iteratively tuning a model. The core steps in
training are

1. Get some data (such as images) from a dataset.
1. Run the data through our model.
1. Adjust our model.
1. Repeat until we're satisfied.

These steps describe what is called the "training loop." Let's codify it and
start building our engine skeleton.

```py
# Training loop.
while not_satisfied:
    # Get some data.
    # Run our model with the data.
    # Adjust the model.
```

We can already start asking important questions. For example, where do the data
and model come from? How does model adjustment work? What are the interfaces of
each part? What is our criteria for being satisfied?

## Keeping the Engine Generic

We could answer the questions above by designing our engine to work with a very
specific model and data.

```py
dataset = create_the_specific_dataset()
model = create_the_specific_model()
i = 0
while i < 1000:
    data = dataset.get_next_data_for_the_specific_model()
    results = model.run(data)
    adjust_the_specific_model(model, results)
```

But a more useful engine allows us to work with a variety of datasets and
models. Such an engine would be more data- and model-agnostic, and its behavior,
such as how many iterations of the training loop to perform, would be
adjustable. Adding parameters to the hypothetical functions above will give us
more control over the functions' behavior. But, we need a way for the user to
provide values for these parameters without hard-coding the values into our
engine. This is done by accepting values from outside the program, such as from
the command line.

As we will see later in this material, there will eventually be a lot of values
to specify. To prevent our command-line interface from becoming unwieldly, we
will have our users provide their custom values in a configuration file and have
them pass the pathname to their configuration on the command line.

To avoid taking on a new dependency, we will use
[JSON](https://www.json.org/json-en.html) as our configuration language as
Python has built-in support for working with it. There are many other options
such as [INI](https://en.wikipedia.org/wiki/INI_file),
[TOML](https://github.com/toml-lang/toml), and [YAML](https://yaml.org/).

Now, the hypothetical `create_the_specific_dataset()` and
`create_the_specific_model()` functions can be turned into factories that take
either a loaded instance of the entire configuration or various arguments the
values of which we take directly from the loaded configuration.

## Training Loop Criteria

For our first addition to our first configuration file, we can specify the
`while not_satisfied` (later `while i < 1000`) criteria. The training loop is
typically run until one of two conditions is met. The first is that we reach a
configured number of iterations. The second is that we determine that some
measured metric of our model meets our expectations before we have reached the
configured number of iterations. We can easily codify the first condition in our
configuration file. Let's do it as

```json
{
  "trainer": {
    "num_iters": 1000
  }
}
```

## Challenge

We haven't covered the interfaces between any of our components yet or what it
actually looks like to load data or a model. So, build the skeleton of the
engine and accomplish at least the following:

1. Implement a command-line interface to get a pathname to a configuration file.
1. Implement a configuration loader. The loader should have the signature
   `load_config(config_pathname: str) -> Dict`.
1. Create the first configuration file that specifies the maximum number of
   trainer iterations.
1. Stub anything left unspecified so far.

As a hint, here is how we'll be structuring our source tree:

```
configs/
engine/
trainer.py
```

JSON configuration will live in `configs/`, library code will live in `engine/`,
and our main program will live in `trainer.py`.

Lastly, note that this challenge is a getting-started exercise and requires very
little code to complete. We'll implement our stubs and connect things together
as we progress through the material.
