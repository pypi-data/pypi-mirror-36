.. vim: set fileencoding=utf-8 :
.. Thu 23 Jun 13:43:22 2016
.. image:: http://img.shields.io/badge/docs-v1.0.0-yellow.svg
   :target: https://www.idiap.ch/software/bob/docs/bob/bob.paper.eusipco2018/v1.0.0/index.html
.. image:: http://img.shields.io/badge/docs-latest-orange.svg
   :target: https://www.idiap.ch/software/bob/docs/bob/bob.paper.eusipco2018/master/index.html
.. image:: https://gitlab.idiap.ch/bob/bob.paper.eusipco2018/badges/v1.0.0/build.svg
   :target: https://gitlab.idiap.ch/bob/bob.paper.eusipco2018/commits/v1.0.0
.. image:: https://img.shields.io/badge/gitlab-project-0000c0.svg
   :target: https://gitlab.idiap.ch/bob/bob.paper.eusipco2018
.. image:: http://img.shields.io/pypi/v/bob.paper.eusipco2018.svg
   :target: https://pypi.python.org/pypi/bob.paper.eusipco2018


===================================================
 Speaker Inconsistency Detection in Tampered Video
===================================================

This package is part of the Bob_ toolkit and it allows to reproduce the experimental results published in the following paper::

    @inproceedings{KorshunovEusipco2018,
        author = {P. Korshunov AND S. Marcel},
        title = {Speaker Inconsistency Detection in Tampered Video},
        year = {2018},
        month = sep,
        booktitle = {{EUSIPCO 2018}},
        address = {Rome, Italy},
    }

If you use this package and/or its results, please cite the paper.


Installation
------------

The installation instructions are based on conda_ and works on **Linux** and **Mac OS** systems
only. `Install conda`_ before continuing.

Once you have installed conda_, download the source code of this paper and
unpack it or checkout from Gitlab.  Then, you can create a conda environment with the following
command::

    $ cd bob.paper.eusipco2018
    $ conda env create -f environment.yml
    $ source activate bob.paper.eusipco2018  # activate the environment
    $ python -c "import bob.bio.base"  # test the installation
    $ buildout

This will install all the required software to reproduce this paper.


Documentation
-------------
For further documentation on this package, please read the `Documentation <https://www.idiap.ch/software/bob/docs/bob/bob.paper.eusipco2018/v1.0.0/index.html>`_.
For a list of tutorials on this or the other packages of Bob_, or information on submitting issues, asking questions and starting discussions, please visit its website.

.. _bob: http://www.idiap.ch/software/bob
.. _conda: https://conda.io
.. _install conda: https://conda.io/docs/install/quick.html#linux-miniconda-install
.. _bob.bio: https://pypi.python.org/pypi/bob.bio.base

