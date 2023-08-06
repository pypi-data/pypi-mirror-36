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
* [`pandas`](https://pandas.pydata.org/)

Depending on the chosen `matplotlib` backend, there may be other dependencies, such as `PySide`/`PySide2` or `PyGTK`.

To install from PyPI:

    pip3 install ecgclock

Or from git:

    git clone https://bitbucket.org/atpage/ecgclock.git
    cd ecgclock
    pip3 install -e .

### How do I run it? ###

See `test_simple_clock()` and `test_complex_clock()` in `test_ecgclock.py`, or run `make_qtclock -h`.  In Windows you should run `multiprocessing.freeze_support()` at the beginning of any `__main__` function.

### Note on API changes: ###

Usage of this library was originally documented in [this article](https://doi.org/10.1109/ACCESS.2015.2509426).  However, significant refactoring of the code is taking place in 2018, including API changes.  The article is still a good reference, but specific code examples will no longer work as-is.

To use the old version of the library, roll back to commit 7e4d4ce (which is tagged as 'old').

### Who do I talk to? ###

* Alex Page, alex.page@rochester.edu
* Jean-Phillippe Couderc, URMC
