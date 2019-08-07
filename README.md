[![Build Status](https://travis-ci.org/jonas-hagen/databird.svg?branch=master)](https://travis-ci.org/jonas-hagen/databird)

# databird

Periodically retrieve data from different sources.

The `databird` package only provides a framework to plan and run the tasks needed to keep a local data-file-store up do date with various remote sources.
The remote sources can be anything (e.g. FTP Server, ECMWF, HTTP Api, SQL database, ...), as long as there is a *databird-driver* available for the specific source.

## Usage

Databird is configured with configuration files and invoked by

```
$ databird retrieve -c /etc/databird/databird.conf

# or (as the above is the default)
$ databird retrieve
```

You can store the configuration files anywhere and for example run the above command periodically as cron job.

Also, some rq workers are required:

```
$ rq worker databird
```

This will start one worker. You should use a supervisor to start multiple workers.

## Configuration

The following example configuration defines a repository, which is populated with daily GNSS data from [ftp://cddis.nasa.gov/gnss/data/daily/](ftp://cddis.nasa.gov/gnss/data/daily/).

The main configuration file (usually `databird.conf`) could look like that:

```yml
general:
  root: /data/repos # root path for data repositories
  num-workers: 16   # max number of async workers
  include: "databird.conf.d/*.conf"  # include config files
```

Generally you can configure anything in any file, as all configuration files are merged to one configuration tree. The `include` option is an exception, as it can only be declared in the top config file.

Then in `databird.conf.d/cddis.conf` you can configure a profile and a repository:

```yml
profiles:
  nasa_cddis:
    driver: standard.FtpDriver
    configuration:
      host: cddis.nasa.gov
      user: anonymous
      password: ""
      tls: False
       
repositories:
  nasa_gnss:
    description: Data from NASAs Archive of Space Geodesy Data
    profile: nasa_cddis
    period: 1 day
    delay: 2 days
    start: 2019-01-01
    targets:
      status: "{time:%Y}/cddis_gnss_{iso_date}.status"
    configuration:
      user: anonymous  # this could override 'user' from profile
      root: "/gnss/data/daily"
      patterns:
        status: "{time:%Y}/{time:%j}/{time:%y%j}.status"
```

When calling databird with this configuration the following is achieved:

* A repository in the folder `/data/repos/nasa_gnss/` is created
* For every day, a file like `2019/nasa_gnss_2019-01-20.status` is expected
* If that file is missing, retrieve it from `ftp://cddis.nasa.gov/gnss/data/daily/2019/020/19020.status`
* If there are many files missing, the data is retrieved asynchronously

This example used the `standard.FTPDriver`.

## Monitoring

Use `databird webmonitor [PORT]` to start the web interface.

Since databird uses RQ for managing jobs, you also check the options at [RQ/docs/monitoring](https://python-rq.org/docs/monitoring/).

## Drivers

Anyone can write drivers (see below). Currently, the following drivers are available:

Included:

* `standard.FilesystemDriver`: Retrieve data from the local filesystem
* `standard.CommandDriver`: Run an arbitrary shell command
* `standard.FtpDriver`: Retrieve data from an FTP server

Climate:

* `climate.EcmwfDriver`: Retrieve data from the European Centre for Medium-Range Weather Forecasts (ECMWF) via their API
* `climate.C3SDriver`: Retrieve data from the Copernicus Climate Change Service (C3S) via their API
* `climate.GesDiscDriver`: Retrieve data from the NASA EarthData GES DISC service.


## Development

1. Create a Python environment and activate it
   ``` shell
   $ python3 -m venv . && source bin/activate
   ```
2. Install the development environment:
   ``` shell
   (databird) $ pip install -r requirements-dev.txt
   ```

### Writing a new driver

Drivers are published in a namespace package `databird-drivers`. Everyone can develop drivers and share them.

Install `databird` and run mr.bob to create a new driver package:

```
(databird) $ cd $HOME/projects
(databird) $ python -m mrbob.cli databird.blueprints:driver
```

After answering some questions, a new directory `databird-driver-<chosen_name>` is created.
Lets asume `<chosen_name> = foo`, then your driver is usually implemented in `databird/drivers/foo/foo.py` in a class named `FooDriver()`.
Until more documentation is available, you have to look at the code to figure out how to write a driver.

Other people will be able to use it with `driver: foo.FooDriver`.

Tell me if you wrote a new driver, so I can include it in the list.
