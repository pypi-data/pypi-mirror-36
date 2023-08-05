XIST provides an extensible HTML and XML generator. XIST is also a XML parser
with a very simple and pythonesque tree API. Every XML element type corresponds
to a Python class and these Python classes provide a conversion method to
transform the XML tree (e.g. into HTML). XIST can be considered
'object oriented XSLT'.

XIST also includes the following modules and packages:

* ``ll.ul4c`` is compiler for a cross-platform templating language with
  similar capabilities to `Django's templating language`__. ``UL4`` templates
  are compiled to an internal format, which makes it possible to implement
  template renderers in other languages and makes the template code "secure"
  (i.e. template code can't open or delete files).

  __ https://docs.djangoproject.com/en/1.5/topics/templates/

  There are implementations for Python, Java and Javascript.

* ``ll.ul4on`` provides functions for encoding and decoding a lightweight
  machine-readable text-based format for serializing the object types supported
  by UL4. It is extensible to allow encoding/decoding arbitrary instances
  (i.e. it is basically a reimplementation of ``pickle``, but with string
  input/output instead of bytes and with an eye towards cross-plattform
  support).

  There are implementations for Python, Java and Javascript.

* ``ll.orasql`` provides utilities for working with cx_Oracle_:

  - It allows calling functions and procedures with keyword arguments.

  - Query results will be put into Record objects, where database fields
    are accessible as object attributes.

  - The ``Connection`` class provides methods for iterating through the
    database metadata.

  - Importing the modules adds support for URLs with the scheme ``oracle`` to
    ``ll.url``.

  .. _cx_Oracle: https://oracle.github.io/python-cx_Oracle/

* ``ll.make`` is an object oriented make replacement. Like make it allows
  you to specify dependencies between files and actions to be executed
  when files don't exist or are out of date with respect to one
  of their sources. But unlike make you can do this in a object oriented
  way and targets are not only limited to files.

* ``ll.color`` provides classes and functions for handling RGB color values.
  This includes the ability to convert between different color models
  (RGB, HSV, HLS) as well as to and from CSS format, and several functions
  for modifying and mixing colors.

* ``ll.sisyphus`` provides classes for running Python scripts as cron jobs.

* ``ll.url`` provides classes for parsing and constructing RFC 2396
  compliant URLs.

* ``ll.nightshade`` can be used to serve the output of PL/SQL
  functions/procedures with CherryPy__.

* ``ll.misc`` provides several small utility functions and classes.

* ``ll.astyle`` can be used for colored terminal output (via ANSI escape
  sequences).

* ``ll.daemon`` can be used on UNIX to fork a daemon process.

* ``ll.xml_codec`` contains a complete codec for encoding and decoding XML.

__ http://www.cherrypy.org/


Changes in 5.35 (released 09/14/2018)
-------------------------------------

* UL4 now support both ``datetime`` and ``date`` objects. A function ``today``
  has been added that returns the current day as a ``date`` object.

* The UL4 method ``week`` for date objects now by default returns the ISO
  calendar week number. The day that should be considered the first day of the
  week and how many days the first week of the year has to have can be passed
  as parameters.

* A new UL4 method ``calendar`` has been added that returns the ISO calendar
  year, the ISO calendar week and the weekday. Similar to ``week`` the day that
  should be considered the first day of the week and how many days the first
  week of the year has to have can be passed as parameters.

* Speed up deserializing strings from UL4ON dumps.

* ``ll.sisyphus`` now uses ``psutil`` to terminate all child processes
  when the maximum runtime is exceeded. If ``psutil`` is not available
  only the forked child process itself will be terminated as before.

* Fixed a bug in ``ll.orasql.ForeignKey.refconstraint`` for foreign keys
  that reference a table in another schema.




