=========================
Pygments AnyScript plugin
=========================

.. image:: https://img.shields.io/travis/AnyBody/pygments-anyscript.svg
    :target: https://travis-ci.org/AnyBody/pygments-anyscript
.. image:: https://img.shields.io/pypi/v/pygments_anyscript.svg
    :target: https://pypi.python.org/pypi/pygments_anyscript
.. image:: https://anaconda.org/conda-forge/pygments_anyscript/badges/version.svg
    :target: https://anaconda.org/conda-forge/pygments_anyscript
.. image:: https://anaconda.org/conda-forge/pygments_anyscript/badges/downloads.svg
    :target: https://anaconda.org/conda-forge/pygments_anyscript


Pygments lexer and style for the AnyScript language. AnyScript is the
scripting langugage used for the AnyBody Modeling System; a system for
multibody musculoskeletal analysis.


Installation
------------

* **Pip:** Run ``pip install pygments-anyscript``
* **Conda:** Run ``conda -c conda-forge pygments_anyscript``
* **Source:** Download source and execute ``python setup.py install``

Requirements
------------

 * pygments

Usage
-----

The lexer and style can be used with the Pygments api like any other lexer or style.

::

  $ pygmentize -l AnyScript MyAnyScriptFile.any
  $ pygmentize -l AnyScript -O style=anyscript MyAnyScriptFile.any
  $ pygmentize -l AnyScript -f html -O full,style=anyscript -o  MyAnyScriptFile.html MyAnyScriptFile.any

