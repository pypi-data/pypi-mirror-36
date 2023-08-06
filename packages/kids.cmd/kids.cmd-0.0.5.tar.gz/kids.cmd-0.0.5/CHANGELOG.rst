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


