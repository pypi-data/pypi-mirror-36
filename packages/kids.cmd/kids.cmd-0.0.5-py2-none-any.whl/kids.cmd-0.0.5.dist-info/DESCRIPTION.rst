=========================
kids.cmd
=========================

.. image:: http://img.shields.io/pypi/v/kids.cmd.svg?style=flat
   :target: https://pypi.python.org/pypi/kids.cmd/
   :alt: Latest PyPI version

.. image:: http://img.shields.io/travis/0k/kids.cmd/master.svg?style=flat
   :target: https://travis-ci.org/0k/kids.cmd/
   :alt: Travis CI build status

.. image:: http://img.shields.io/coveralls/0k/kids.cmd/master.svg?style=flat
   :target: https://coveralls.io/r/0k/kids.cmd
   :alt: Test coverage



``kids.cmd`` is a Python library providing helpers when writing command
line utilities in python.

It's part of 'Kids' (for Keep It Dead Simple) library.


Maturity
========

This code is in alpha stage. It wasn't tested on Windows. API may change.
This is more a draft for an ongoing reflection.

And I should add this is probably not ready to show. Although, a lot of these
function are used everyday in my projects and I got sick rewritting them for
every project.


Features
========

using ``kids.cmd``:

- Leverage `docopt`_ library to let you write once your help and usage
  doc, and the parsing will be done automatically from this same
  description.
- Uses kids.ansi to provide nice colored output.
- Nice user input, one key press or more, with built-in menus.

These assumptions are in the code:

- You don't wan't to mess with parsing the command line and will use
  standard command line compatible with docopt command line.
- You like having a very simple paradigm with default behavior that
  you can learn after.

.. _docopt: http://docopt.org/


Compatibility
=============

Tis code is python2 and python3 ready. It wasn't tested on windows.


Installation
============

You don't need to download the GIT version of the code as ``kids.cmd`` is
available on the PyPI. So you should be able to run::

    pip install kids.cmd

If you have downloaded the GIT sources, then you could add install
the current version via traditional::

    python setup.py install

And if you don't have the GIT sources but would like to get the latest
master or branch from github, you could also::

    pip install git+https://github.com/0k/kids.cmd

Or even select a specific revision (branch/tag/commit)::

    pip install git+https://github.com/0k/kids.cmd@master


Usage
=====

TBD


Contributing
============

Any suggestion or issue is welcome. Push request are very welcome,
please check out the guidelines.


Push Request Guidelines
-----------------------

You can send any code. I'll look at it and will integrate it myself in
the code base and leave you as the author. This process can take time and
it'll take less time if you follow the following guidelines:

- check your code with PEP8 or pylint. Try to stick to 80 columns wide.
- separate your commits per smallest concern.
- each commit should pass the tests (to allow easy bisect)
- each functionality/bugfix commit should contain the code, tests,
  and doc.
- prior minor commit with typographic or code cosmetic changes are
  very welcome. These should be tagged in their commit summary with
  ``!minor``.
- the commit message should follow gitchangelog rules (check the git
  log to get examples)
- if the commit fixes an issue or finished the implementation of a
  feature, please mention it in the summary.

If you have some questions about guidelines which is not answered here,
please check the current ``git log``, you might find previous commit that
would show you how to deal with your issue.


License
=======

Copyright (c) 2018 Valentin Lab.

Licensed under the `BSD License`_.

.. _BSD License: http://raw.github.com/0k/kids.cmd/master/LICENSE

Changelog
=========


0.0.5 (2018-09-25)
------------------

New
~~~
- Support of complex ``\*_DEBUG`` values to fine tune logging. [Valentin
  Lab]

  Environment variable in ``<exname>_DEBUG`` now supports strings like:
  "my.module:DEBUG,my.other.module:WARN". Of course, logging messages
  should use python ``logging`` module.

Fix
~~~
- Better namespacing scheme. [Valentin Lab]

  The previous would import ``pkg_resources`` which could take
  some linear time depending on the number of installed packages.

Other
~~~~~
- Pkg: fix: include LICENSE in final package. [Valentin Lab]


0.0.4 (2016-03-03)
------------------

New
~~~
- [cmd] support finding module even when called through command
  entrypoints. [Valentin Lab]
- [cmd] support for discovering module commands in ``pkg_resources``
  eggs. [Valentin Lab]

  Previously, command were not discovered if your command got packaged to
  a single file zipped egg.


0.0.3 (2015-03-12)
------------------

New
~~~
- [cmd] add ``exname`` to args ``__env__`` sent to sub commands.
  [Valentin Lab]
- [cmd] catches uncaught exception and hide the full traceback except if
  debug environment variable set. [Valentin Lab]

Changes
~~~~~~~
- [cmd] ``.cfg`` provides read/write access to config files. [Valentin
  Lab]

Fix
~~~
- [menu] line call would fail because of incorrect call to
  ``kids.ansi``. [Valentin Lab]
- Fixed bunch of bugs on argument attribution. [Valentin Lab]

  Added thorough tests on the facility.


0.0.2 (2015-02-06)
------------------
- First import. [Valentin Lab]



