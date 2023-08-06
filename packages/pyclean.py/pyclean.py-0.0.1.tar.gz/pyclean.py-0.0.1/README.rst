===============================================================================
pyclean.py: Clean compiled from a Python project.
===============================================================================

To install::

    pip install pyclean.py


Example usages::

    # Clean files related to "src/pip/__init__.py".
    pyclean src/pip/__init__.py

    # Clean files for every Python file in the directory "src", recursively.
    pyclean src



An extra script named ``py-clean`` is provided in addition to ``pyclean``,
to avoid command name conflicts with pyclean_ in Debian.


.. _pyclean: https://manpages.debian.org/jessie/python-minimal/pyclean.1.en.html
