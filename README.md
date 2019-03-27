# databird

Periodically retrieve data from different sources.

## Setup

### Setting up the development environment

1. Create a Python environment and activate it
   ``` shell
   $ python3 -m venv . && source bin/activate
   ```
2. Install the development environment:
   ``` shell
   (databird) $ pip install -r requirements/development.txt
   ```

## Writing a new driver

Install `databird` and run mr.bob to create a new driver package:

```
(databird) $ cd $HOME/projects
(databird) $ python -m mrbob.cli databird.blueprints:driver
```

After answering some questions, a new directory `databird-driver-<chosen_name>` is be created.
Lets asume `<chosen_name> = foo`, then your driver is usually implemented in `databird/drivers/foo/foo.py` in a class named `FooDriver()`.

Other people will be able to use it with `driver: foo.FooDriver`.
