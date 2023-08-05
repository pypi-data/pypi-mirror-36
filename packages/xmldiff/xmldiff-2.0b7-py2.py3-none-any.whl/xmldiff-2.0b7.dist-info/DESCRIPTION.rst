xmldiff
========

.. image:: https://travis-ci.org/Shoobx/xmldiff.svg?branch=master

.. image:: https://coveralls.io/repos/github/Shoobx/xmldiff/badge.svg

``xmldiff`` is a library and a command-line utility for making diffs out of XML.
This may seem like something that doesn't need a dedicated utility,
but change detection in hierarchical data is very different from change detection in flat data.
XML type formats are also not only used for computer readable data,
it is also often used as a format for hierarchical data that can be rendered into human readable formats.
A traditional diff on such a format would tell you line by line the differences,
but this would not be be readable by a human.
This library provides tools to make human readable diffs in those situations.


Quick usage
-----------

``xmldiff`` is both a command-line tool and a Python library.
To use it from the command-line, just run ``xmldiff`` with two input files::

  $ xmldiff file1.xml file2.xml

As a library::

  from lxml import etree
  from xmldiff import main, formatting

  differ = diff.Differ()
  diff = main.diff_files('file1.xml', 'file2.xml',
                         formatter=formatting.XMLFormatter())

  print(diff)

There is also a method ``diff_trees()`` that take two lxml trees,
and a method ``diff_texts()`` that will take strings containing XML.


Changes from ``xmldiff`` 0.6/1.x
--------------------------------

  * A complete, ground up, pure-Python rewrite

  * Easier to maintain, the code is less complex and more Pythonic,
    and uses more custom classes instead of just nesting lists and dicts.

  * Fixes the problems with certain large files and solves the memory leaks.

  * A nice, easy to use Python API for using it as a library.

  * Adds support for showing the diffs in different formats,
    mainly one where differences are marked up in the XML,
    useful for making human readable diffs.

  * These formats can show text differences in a semantically meaningful way.

  * The default output format of the command line tool now does not require
    you to parse the output to apply it. An output format compatible with
    0.6 / 1.x is also available.

  * 2.0 is urrently significantly slower than ``xmldiff`` 0.6/1.x,
    but this will change in the future.
    Currently we make no effort to make ``xmldiff`` 2.0 fast,
    we concentrate on making it correct and usable.


Contributors
------------

 * Lennart Regebro, lregebro@shoobx.com (main author)

 * Stephan Richter, srichter@shoobx.com

The diff algorithm is based on "`Change Detection in Hierarchically Structured Information <http://ilpubs.stanford.edu/115/1/1995-46.pdf>`_",
and the text diff is using Google's ``diff_match_patch`` algorithm.

Changes
=======

2.0b7 (2018-09-14)
------------------

- Renamed and then moved tags will no longer get both insert and delete tags.

- Added an XmlDiffFormatter that gives a format using the old xmldiff output.
  This can be used with "-f old" from the command line.

- UpdateTextIn on a node marked as being inserted will just be inserted,
  not wrapped in extra insert tags.


2.0b6 (2018-09-13)
------------------

- Release of 2.0b5 failed, re-releasing.


2.0b5 (2018-09-13)
------------------

- Many more edge case bugs


2.0b4 (2018-09-12)
------------------

- Fixed some edge case bugs


2.0b3 (2018-09-11)
------------------

- Replaced the example RMLFormatter with a more generic HTML formatter,
  although it only handles HTML snippets at the moment.

- Added a RenameNodeAction, to get rid of an edge case of a node
  tail appearing twice.


2.0b2 (2018-09-06)
------------------

- Documentation

- The diff formatter now handles the --keep-whitespace argument

- Added a ``--version`` argument


2.0b1 (2018-09-03)
------------------

- A complete, bottom-up, pure-python rewrite

- New easy API

- New output formats:

  - A list of actions (similar but not compatible with the old format)

  - XML with changes marked though tags and attributes

  - RML aware XML where tags containing text are semantically diffed, useful
    for human output such as converting to HTML or PDF

- 100% test coverage


