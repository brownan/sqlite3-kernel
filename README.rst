A simple Jupyter kernel for SQLite3

This requires IPython 3 and the sqlite3 command line tool to be installed.

To install::

    python setup.py install
    python -m sqlite3_kernel.install

To use it, run one of:

.. code:: shell

    jupyter notebook
    # In the notebook interface, select SQLite3 from the 'New' menu
    jupyter qtconsole --kernel sqlite3
    jupyter console --kernel sqlite3

For details of how this works, see the Jupyter docs on `wrapper kernels
<http://jupyter-client.readthedocs.org/en/latest/wrapperkernels.html>`_, and
Pexpect's docs on the `replwrap module
<http://pexpect.readthedocs.org/en/latest/api/replwrap.html>`_

Based on the `Bash kernel <https://github.com/takluyver/bash_kernel>`_

Note: this was just a quick and dirty experiment in writing Jupyter kernels.
I decided to publish it on Github in the hopes that others find it useful.
It may not work for everyone, but feel free to use this as a base for
something more robust.
