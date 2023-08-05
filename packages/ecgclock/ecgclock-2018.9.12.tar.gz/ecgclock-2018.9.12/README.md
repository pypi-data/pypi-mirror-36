# ECG Clock Plotter #

This repository contains a python library for simple plotting of ECG data (typically QTc values) in the "24 hour clock" format:

![Example QT Clock](https://bitbucket.org/atpage/ecgclock/raw/master/data/example/baseline_vs_drug.png)

### DISCLAIMER: ###

All of the included default values, ranges, example data sets, etc. are for illustration, not for diagnostic use.  It is the clinician's responsibility to adjust all settings appropriately.

### How do I get set up? ###

You will need Python 3 with the following modules available:

* [`numpy`](http://www.numpy.org/)
* [`dateutil`](http://labix.org/python-dateutil)
* [`matplotlib`](http://matplotlib.org/)
* [`cycler`](http://matplotlib.org/cycler/)

Depending on the chosen `matplotlib` backend, there may be other dependencies, such as `PySide` or `PyGTK`.

To install from PyPI:

    pip3 install ecgclock

Or from git:

    git clone https://bitbucket.org/atpage/ecgclock.git
    cd ecgclock
    pip3 install -e .

### How do I run it? ###

See `test_single_clock()` and `test_subplots_clock()` in `test_ecgclock.py`, or run `make_qtclock -h`.

### Who do I talk to? ###

* Alex Page, alex.page@rochester.edu
* Jean-Phillippe Couderc, URMC
