.. _meshio: https://github.com/nschloe/meshio

Create & Convert *Cubed-sphere Grids* (CSGrid) to Unstructured Meshes
=====================================================================

.. image:: https://img.shields.io/pypi/v/csgrid2unstr.svg
    :target: https://pypi.org/project/csgrid2unstr/
.. image:: https://img.shields.io/pypi/l/csgrid2unstr.svg
    :target: https://pypi.org/project/csgrid2unstr/

Introduction
------------

The grid generator is from `here <https://gist.github.com/darothen/8bf53b448790f21f616552b45ee3b22b>`_,
and I/O is handled by `meshio`_.

This package was created for education/research purpose. Personally, I use this
to study the grid convergence for data transferring between CSGrid and
*spherical centroidal Voronoi tessellations* (SCVT).


.. image:: demo.png
    :scale: 10 %
    :align: center

Installation
------------

You can easily install this package through pip, i.e.

.. code-block:: console

    $ pip install csgrid2unstr --user

You can, of course, install it directly from the repository:

.. code-block:: console

    $ git clone https://github.com/chiao45/csgrid2unstr.git
    $ cd csgrid2unstr && python setup.py install --user

Notice that this package depends on:

1. `numpy <http://www.numpy.org/>`_
2. `setuptools <https://github.com/pypa/setuptools>`_
3. `meshio`_

Usage
-----

As Executable Binary
++++++++++++++++++++

Once you have installed the package, open the terminal and type:

.. code-block:: console

    $ csgrid2unstr -h
    usage: csgrid2unstr [-h] [-n SIZE] [-o OUTPUT] [-r REFINE]
                    [-f {vtk,vtu,gmsh,off,exodus,xdmf,dolfin-xml,stl}] [-b]
                    [-V] [-v]

    write CSGrid to unstr

    optional arguments:
      -h, --help            show this help message and exit
      -n SIZE, --size SIZE  Number of intervals of a square face
      -o OUTPUT, --output OUTPUT
                            Output file name, w/o extension
      -r REFINE, --refine REFINE
                            Level of refinements, default is 1
      -f {vtk,vtu,gmsh,off,exodus,xdmf,dolfin-xml,stl}, --format {vtk,vtu,gmsh,off,exodus,xdmf,dolfin-xml,stl}
                            Output file format, default is VTK
      -b, --binary          Use BINARY. Notice that this flag is ignored for
                            some formats
      -V, --verbose         Verbose output
      -v, --version         Check version

If you got ``command not found: csgrid2unstr``, make sure ``csgrid2unstr`` is
in your ``$PATH``.

There are two must-provided parameters, i.e. ``-n`` (``--size``) and ``-o``
(``--output``). The former is to define the number of intervals of a square
face, i.e. the number of quadrilaterals of a face is n*n, and the latter is
to provide the output filename (**without extension**). For instance:

.. code-block:: console

    $ csgrid2unstr -n 20 -o demo

will construct a CSGrid of 400 quadrilaterals per face, convert the grid into
an unstructured mesh and store it in ``demo.vtk``.

You can create a serial of uniform refined grids by adding ``-r``
(``--refine``) switch, e.g.:

.. code-block:: console

    $ csgrid2unstr -n 10 -r 3 -o demo -f xdmf

will construct three CSGrids with 100, 400, and 1600 quadrilaterals per face,
convert them into three unstructured meshes and store them in ``demo0.xdmf``,
``demo1.xdmf``, and ``demo2.xdfm``, resp.

As Module
+++++++++

Using ``csgrid2unstr`` as a Python module is also simple.

.. code-block:: python

    from __future__ import print_function
    from csgrid2unstr.cubed_sphere import CSGrid
    from csgrid2unstr.unstr import Unstr

    # create a CSGrid of 25 quads per face
    cs = CSGrid(5)

    # convert it into an unstructured mesh
    mesh = Unstr(cs)

    # two attributes, points and cells, of np.ndarray

    print('Nodes {}-by-3'.format(len(mesh.points)))
    print(mesh.points)

    print('Cells {}-by-4'.format(len(mesh.cells)))
    print(mesh.cells)

License
-------

MIT License

Copyright (c) 2018 Qiao Chen
