.. image:: https://readthedocs.org/projects/pip/badge/?version=latest
   :target: https://gxformat2.readthedocs.org

.. image:: https://badge.fury.io/py/gxformat2.svg
   :target: https://pypi.python.org/pypi/gxformat2/

.. image:: https://travis-ci.org/jmchilton/gxformat2.png?branch=master
   :target: https://travis-ci.org/jmchilton/gxformat2

.. image:: https://coveralls.io/repos/jmchilton/gxformat2/badge.svg?branch=master
   :target: https://coveralls.io/r/jmchilton/gxformat2?branch=master


This package defines a high-level Galaxy_ workflow description termed "Format
2". At this point, these workflows are defined entirely client side and
transcoded into traditional (or Format 1?) Galaxy workflows.

The traditional Galaxy workflow description is not meant to be concise and is
neither readily human readable or human writable. Format 2 addresses all three
of these limitations.

Format 2 workflow is a highly experimental format and will change rapidly in
potentially backward incompatible ways until the code is merged into the
Galaxy server and enabled by default.

* Free software: Academic Free License version 3.0
* Documentation: https://galaxy-lib.readthedocs.org.
* Code: https://github.com/galaxyproject/galaxy-lib


.. _Galaxy: http://galaxyproject.org/
.. _GitHub: https://github.com/
.. _Travis CI: http://travis-ci.org/




History
-------

.. to_doc

---------------------
0.3.0 (2018-09-30)
---------------------

* More cwl style inputs, initial work on conversion from native workflows, various small fixes and tweaks.

---------------------
0.2.0 (2018-02-21)
---------------------

* Bring in latest Galaxy updates - Python 3 fixes, safe YAML usage, and more PJA implemented.

---------------------
0.1.1 (2016-08-15)
---------------------

* Fix one Python 3 incompatibility.

---------------------
0.1.0 (2016-05-02)
---------------------

* Initial version - code from Galaxy's test framework with changes
  based on planemo testing.


