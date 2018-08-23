Contributing
============

.. sectionauthor:: Matt Swain <m.swain@me.com>

Contributions of any kind are greatly appreciated!

Feedback
--------

The `Issue Tracker`_ is the best place to post any feature ideas, requests and bug reports.

Contributing
------------

If you are able to contribute changes yourself, just fork the `source code`_ on GitHub, make changes and file a pull
request. All contributions are welcome, no matter how big or small.

Quick guide to contributing
~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. `Fork the ChemSpiPy repository on GitHub`_, then clone your fork to your local machine::

    git clone https://github.com/<username>/ChemSpiPy.git
    cd ChemSpiPy

2. Install the development requirements into a `conda environment`_::

    conda env create -n chemspipy -f environment.yml
    source activate chemspipy

3. Create a new branch for your changes::

    git checkout -b <name-for-changes>

4. Make your changes or additions. Ideally add some tests and ensure they pass by running::

    pytest

5. Commit your changes and push to your fork on GitHub::

    git add .
    git commit -m "<description-of-changes>"
    git push origin <name-for-changes>

4. `Submit a pull request`_.

Tips
~~~~

- Follow the `PEP8`_ style guide.
- Include docstrings as described in `PEP257`_.
- Try and include tests that cover your changes.
- Try to write `good commit messages`_.
- Read the GitHub help page on `Using pull requests`_.

.. _`Issue Tracker`: https://github.com/mcs07/ChemSpiPy/issues
.. _`source code`: https://github.com/mcs07/ChemSpiPy
.. _`Fork the ChemSpiPy repository on GitHub`: https://github.com/mcs07/ChemSpiPy/fork
.. _`conda environment`: https://conda.io/docs/
.. _`Submit a pull request`: https://github.com/mcs07/ChemSpiPy/compare/
.. _`PEP8`: https://www.python.org/dev/peps/pep-0008
.. _`PEP257`: https://www.python.org/dev/peps/pep-0257
.. _`good commit messages`: https://tbaggery.com/2008/04/19/a-note-about-git-commit-messages.html
.. _`Using pull requests`: https://help.github.com/articles/using-pull-requests
