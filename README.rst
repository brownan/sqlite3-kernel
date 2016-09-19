A simple Jupyter kernel for SQLite3

This requires IPython 3.

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
