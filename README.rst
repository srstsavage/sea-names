
.. image:: http://git.axiom/axiom/sea-names/badges/main/pipeline.svg
   :alt: Pipeline status

sea-names
===============================

Determine the sea-name of any arbitrary point or shapely geometry.

Copyright 2023 Axiom Data Science, LLC

See LICENSE for details.

Installation
------------

This project relies on conda for installation and managing of the project dependencies.

1. Download and install miniconda for your operating system https://docs.conda.io/en/latest/miniconda.html.

2. Clone this project with ``git``.

3.  Once conda is available build the environment for this project with::

      conda env create -f environment.yml

    The above command creates a new conda environment titled ``sea-names`` with the necessary project
    dependencies.

4. An Additional environment file is present for testing and development environments. The additional developer dependencies can be installed with::

      conda env update -f test-environment.yml

5. To install the project to the new environment::

      conda activate sea-names
      pip install -e .

Running Tests
-------------

To run the project's tests::

   pytest -sv --integration

Usage
-----


Configuration
-------------



Building with Docker
--------------------

To build the docker container::

   docker build -t sea-names .

Running with Docker
-------------------

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
