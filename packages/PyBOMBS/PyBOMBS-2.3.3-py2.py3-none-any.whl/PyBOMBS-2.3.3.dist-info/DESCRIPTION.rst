PyBOMBS
~~~~~~~

PyBOMBS (the Python Bundles Overlay Managed Build System) is a meta-package
manager that can install packages from source or using the local package
manager(s).

It was mainly designed for use by users of the `GNU Radio project`_, which
is extended by a large number of out-of-tree modules (OOTs).

PyBOMBS is a recipe-based system and can easily mix and match installations
from different sources. Cross-compilation works transparently.


Basic commands
--------------

With PyBOMBS installed, you might want to install GNU Radio into a directory
called `my_gnuradio`. First, you create a /prefix/ there:

    $ pybombs prefix init my_gnuradio

Then, you call PyBOMBS to do the installation:

    $ pybombs install gnuradio

PyBOMBS will determine the dependency tree for GNU Radio, and install
dependencies either through the local system's package manager (e.g.
apt, yum, pip...) or pull the source files and build them in the
prefix.

With slight modifications, the same commands would have worked to create
a cross-compile environment and cross-compile GNU Radio:

    $ pybombs prefix init my_gnuradio --sdk e300
    $ pybombs install gnuradio

For more informations see the `documentation`_.

.. _GNU Radio project: http://gnuradio.org/
.. _documentation: https://www.gnuradio.org/blog/pybombs-the-what-the-how-and-the-why/


