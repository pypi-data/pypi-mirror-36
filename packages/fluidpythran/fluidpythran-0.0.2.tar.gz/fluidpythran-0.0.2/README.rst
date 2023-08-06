FluidPythran: Pythran annotations in Python files
=================================================

|release| |coverage|

.. |release| image:: https://img.shields.io/pypi/v/fluidpythran.svg
   :target: https://pypi.python.org/pypi/fluidpythran/
   :alt: Latest version

.. |coverage| image:: https://codecov.io/bb/fluiddyn/fluidpythran/branch/default/graph/badge.svg
   :target: https://codecov.io/bb/fluiddyn/fluidpythran/branch/default/
   :alt: Code coverage


.. warning ::

   This is really just a prototype. See `this post
   <http://www.legi.grenoble-inp.fr/people/Pierre.Augier/broadcasting-numpy-abstraction-cython-pythran-fluidpythran.html>`_
   (and also `this method
   <https://bitbucket.org/fluiddyn/fluidsim/src/c0e170ea7c68f2abc4b0f7749b1c89df79db6573/fluidsim/base/time_stepping/pseudo_spect.py#lines-240>`_)
   for an explanation of my motivations.

This pure-Python package will provide few supplementary pythran commands,
namely :code:`pythran block` and :code:`pythran def` (see examples in the doc
folder).

The code of the numerical kernels can stay in the modules and in the classes
where they were written. The Pythran files (i.e. the files compiled by
Pythran), which are usually written by the user, are produced automatically.

The code continues to work fine without Pythran, which is used only when
available.

Installation
------------

.. code ::

   pip install fluidpythran

License
-------

FluidDyn is distributed under the CeCILL-B_ License, a BSD compatible
french license.

.. _CeCILL-B: http://www.cecill.info/index.en.html
