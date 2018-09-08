.. _install:

Installation
============

ChemSpiPy supports Python versions 2.7 and 3.5+.

There are two required dependencies: `six`_ and `requests`_.

Option 1: Use conda (recommended)
---------------------------------

The easiest and recommended way to install is using conda. `Anaconda Python`_ is a self-contained Python environment
that is particularly useful for scientific applications. If you don't already have it, start by installing `Miniconda`_,
which includes a complete Python distribution and the conda package manager. Choose the Python 3 version, unless you
have a particular reason why you must use Python 2.

To install ChemSpiPy, at the command line, run::

    conda config --add channels conda-forge
    conda install chemspipy

This will add the `conda-forge`_ channel to your conda config, then install ChemSpiPy and all its dependencies into your
conda environment.

Option 2: Use pip
-----------------

An alternative method is to install using pip::

    pip install chemspipy

This will download the latest version of ChemSpiPy, and place it in your `site-packages` folder so it is automatically
available to all your python scripts. It should also ensure that the dependencies `six`_ and `requests`_ are installed.

If you don't already have pip installed, you can `install it using get-pip.py`_::

       curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
       python get-pip.py

Option 3: Download the Latest Release
-------------------------------------

Alternatively, `download the latest release`_ manually and install yourself::

    tar -xzvf ChemSpiPy-1.0.5.tar.gz
    cd ChemSpiPy-1.0.5
    python setup.py install

The setup.py command will install ChemSpiPy in your `site-packages` folder so it is automatically available to all your
python scripts.

Option 4: Clone the Repository
------------------------------

The latest development version of ChemSpiPy is always `available on GitHub`_. This version is not guaranteed to be
stable, but may include new features that have not yet been released. Simply clone the repository and install as usual::

    git clone https://github.com/mcs07/ChemSpiPy.git
    cd ChemSpiPy
    python setup.py install

.. _`six`: http://pythonhosted.org/six/
.. _`requests`: http://docs.python-requests.org/
.. _`Anaconda Python`: https://www.anaconda.com/distribution/
.. _`Miniconda`: https://conda.io/miniconda.html
.. _`conda-forge`: https://conda-forge.org/
.. _`install it using get-pip.py`: https://pip.pypa.io/en/stable/installing/
.. _`download the latest release`: https://github.com/mcs07/ChemSpiPy/releases/
.. _`available on GitHub`: https://github.com/mcs07/ChemSpiPy
