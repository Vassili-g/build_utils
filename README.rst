
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

pip
~~~~~

The recommended way to install this library is::

	pip install build_utils

Development
~~~~~~~~~~~~~

If you wish to develop and submit git-pulls, you can do::

	git clone https://github.com/walchko/build_utils
	cd build_utils
	pip install -e .

Usage
--------

To use this package, add the following to your ``setup.py``:

.. code-block:: python

	PACKAGE_NAME = 'build_utils'
	BuildCommand.pkg = PACKAGE_NAME
	BuildCommand.test = False
	PublishCommand.pkg = PACKAGE_NAME
	PublishCommand.version = VERSION

Take a look at the setup for this library on ``github`` for an example. Note
that by default, testing and both py2 and py3 are ``True`` by default.
Now you can build and publish a new package by::

	python setup.py make
	python setup.py publish

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
