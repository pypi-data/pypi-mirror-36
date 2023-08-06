|package-version|

|python-versions|

|circle-ci-badge| |codecov| |Documentation Status|

Pymox is an open source mock object framework for Python.

First Steps
-----------

`Installation <http://pymox.readthedocs.io/en/latest/install.html>`__
`Tutorial <http://pymox.readthedocs.io/en/latest/tutorial.html>`__

Documentation
-------------

http://pymox.readthedocs.io/en/latest/index.html

Community
---------

User and developer discussion group:

http://groups.google.com/group/mox-discuss

Disclaimer
----------

Pymox is a fork of Mox. Mox is Copyright 2008 Google Inc, and licensed
under the Apache License, Version 2.0; see the file COPYING for details.
If you would like to help us improve Mox, join the group.

.. |package-version| image:: https://badge.fury.io/py/pymox.svg
.. |python-versions| image:: https://img.shields.io/pypi/pyversions/pymox.svg
.. |circle-ci-badge| image:: https://circleci.com/gh/ivancrneto/pymox.svg?style=shield&circle-token=:circle-tokena7354b480e49feb7bcf87039e32ddae07379f344
.. |codecov| image:: https://codecov.io/gh/ivancrneto/pymox/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/ivancrneto/pymox
.. |Documentation Status| image:: https://readthedocs.org/projects/pymox/badge/?version=latest
   :target: http://pymox.readthedocs.io/en/latest/?badge=latest

Changelog
=========

0.8.0
------------------

* General improvements to PyPI setup.py, including long description
* Added CHANGELOG
* Removed reprecated testing functions
* Rearranged files to a better packaging organization

0.7.8
------------------

* Improved classes and functions descriptions

0.7.7
------------------

* Improved docs
* Small fixes

0.7.6
------------------

* Improvements for detecting and displaying classes and functions descriptions

0.7.5
------------------

* Moved the code to use 4 spaces and to be flake8 compliant

0.7.4
------------------

* Another small fix to handle setup package version dinamically

0.7.3
------------------

* Small fix to handle setup package version dinamically

0.7.2
------------------

* Added support to multiple versions of Python: 2.7, 3.3, 3.4, 3.5
* Added first documentation initiative with a Read the Docs page


0.5.3
------------------

* Added more detailed exceptions
* Detected when an unexpected exception raised during a test to consider as a failed test
* Make it possible to stub out a whole class and its properties and methods with mocks
* Added more comparators


0.5.2
------------------

* Provided logic for mocking classes that are iterable
* Tweaks, bugs fixes and improvements

0.5.1
------------------

* Added first README
* Added __str__ and __repr__ to Mox class
* Added a call checker for args and kwargs passed to functions
* Added a Not comparator
* Making it possible to mock container classes

0.5.0
------------------

* First release


