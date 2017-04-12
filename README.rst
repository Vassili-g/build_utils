
build_utils
============================

.. image:: https://landscape.io/github/walchko/build_utils/master/landscape.svg?style=flat
   :target: https://landscape.io/github/walchko/build_utils/master
   :alt: Code Health
.. image:: https://img.shields.io/pypi/v/build_utils.svg
    :target: https://pypi.python.org/pypi/build_utils/
    :alt: Latest Version
.. image:: https://img.shields.io/pypi/l/build_utils.svg
    :target: https://pypi.python.org/pypi/build_utils/
    :alt: License
.. image:: https://img.shields.io/pypi/pyversions/build_utils.svg
	:target:  https://pypi.python.org/pypi/build_utils/


There is a lot of boiler plate code I would write over and over for my projects,
especially when I try to support both ``python2`` and ``python3``. This project
aims to simplify it and allows me to easily add update/improvements to all of my
projects at once.

Install
-----------

Most systems come with ``python2`` installed, but if you plan on doing ``python3`` development
then you should install that for your platform. For macOS::

	brew install python3

pip
~~~~~

The recommended way to install this library is with ``pip``::

	pip install build_utils

Development
~~~~~~~~~~~~~

If you wish to develop and submit git-pulls, you can do::

	git clone https://github.com/walchko/build_utils
	cd build_utils
	pip install -e .

Usage
--------

To use this package, at a minimum, set your repo up like::

	myLibrary/
	|
	+- myLibrary/
	|   |
	|   +- src files
	+- tests/
	|   |
	|   +- test.py
	+- setup.py

Also add the following to your ``setup.py``:

.. code-block:: python

	... other imports ...
	from build_utils import BuildCommand
	from build_utils import PublishCommand
	from build_utils import BinaryDistribution

	VERSION = '1.0.0'
	PACKAGE_NAME = 'myLibrary'
	
	# class to test and build the module
	BuildCommand.pkg = PACKAGE_NAME
	BuildCommand.test = True  # run all tests, True by default
	BuildCommand.py2 = True   # test and build python2, True by default
				  # note, the test variable above controls if the tests are run
	BuildCommand.py3 = True   # test and build python3, True by default
	
	# class to publish the module to PyPi
	PublishCommand.pkg = PACKAGE_NAME
	PublishCommand.version = VERSION
	
	setup(
		name=PACKAGE_NAME,
		version=VERSION,
		... other options ...
		cmdclass={
			'publish': PublishCommand,  # run this to publish to pypi
			'make': BuildCommand  # run this to test/build library
		}
	)

Take a look at the setup for this library on ``github`` for an example. Note
that by default, testing and both py2 and py3 are ``True`` by default.
Now you can build and publish a new package by::

	python setup.py make
	python setup.py publish

Tests
~~~~~~~~~

This uses ``nose`` to run tests and issues the command ``python -m nose -w tests -v test.py`` where ``python`` will be either ``python2`` or ``python3`` depending on what you enabled.

Now if you have more than one test file, try:

.. code-block:: python

	# assume you have test1.py, test2.py and test3.py ... do:
	from .test1 import *
	from .test2 import *
	from .test3 import *

And all should work fine.

Publishing
------------

This uses ``twine`` by default. Ensure you have a config file setup like in your home directory::

	[distutils]
	index-servers = pypi

	[pypi]
	repository: https://pypi.python.org/pypi
	username: my-awesome-username
	password: super-cool-passworld


Change Log
-------------

============ ======= ============================
2017-04-09   0.1.0   init
============ ======= ============================


MIT License
--------------

Copyright (c) 2017 Kevin J. Walchko

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
