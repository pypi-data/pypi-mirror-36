===================
 icemac.songbeamer
===================

.. image:: https://travis-ci.com/icemac/icemac.songbeamer.svg?branch=master
    :target: https://travis-ci.com/icemac/icemac.songbeamer
.. image:: https://coveralls.io/repos/github/icemac/icemac.songbeamer/badge.svg?branch=master
    :target: https://coveralls.io/github/icemac/icemac.songbeamer?branch=master

Library to read and write `SongBeamer`_ files.

.. contents::

Supported SongBeamer versions
=============================

Currently Songbeamer version 2 to 4 is supported. (Internal version
number in .sng files: ``#Version=3``.)

.. _`SongBeamer` : http://songbeamer.com

Supported Python version
========================

Runs on Python 3.5 up to 3.7 and PyPy3. Older Python versions are not
supported.

Running Tests
=============

To run the tests call::

  $ tox

(You maybe have to install `tox` beforehand using: ``pip install tox``.)

Hacking
=======

Fork me on: https://github.com:/icemac/icemac.songbeamer


=========
 Changes
=========

0.3 (2018-10-07)
================

- Add support for Python 3.5 to 3.7 and PyPy3.

- Drop support for Python 3.2 and 3.3.


0.2.0 (2012-10-31)
==================

- Add ability to parse bytes objects.

- Sorting keys in export file to be compatible across Python 3.2 and 3.3.


0.1.0 (2012-05-05)
==================

- Initial public release.




=======
 To do
=======

Implementations
===============

* import/export of .col files (schedules)


Open Questions
==============

* Are `Transpose` and `Speed` actually int values?


=======
 Usage
=======

Importing a .sng file
=====================

To import a .sng file use the ``parse`` class method. It expects a byte
stream (io.BytesIO or open file) or a bytes object as argument to read from:

  >>> from icemac.songbeamer import SNG
  >>> with open('example.sng', 'rb') as file:
  ...     sng = SNG.parse(file)

  >>> with open('example.sng', 'rb') as file:
  ...     sng = SNG.parse(file.read())


Accessing a file's data
=======================

The parsed data is stored in the ``data`` attribute of the object:

  >>> from pprint import pprint
  >>> pprint(sng.data)
  {'Author': 'me',
   'Text': ['La la la', '---', 'Lei lei lei'],
   'Version': 3}

To access the raw values imported from the .sng file get them using `getattr`:

  >>> sng.Version
  b'3'

Exporting a .sng file
=====================

  >>> from tempfile import TemporaryFile

To export to a .sng file use the ``export`` method. It expects a byte stream (io.BytesIO or open file) as argument to write into:

  >>> with TemporaryFile() as file:
  ...     sng.export(file)
  ...     _ = file.seek(0)
  ...     pprint(file.readlines())
  [b'#Author=me\r\n',
   b'#Version=3\r\n',
   b'---\r\n',
   b'La la la\r\n',
   b'---\r\n',
   b'Lei lei lei']




