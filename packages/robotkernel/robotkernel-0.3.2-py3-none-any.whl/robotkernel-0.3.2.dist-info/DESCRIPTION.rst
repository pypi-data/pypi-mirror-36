Robot Framework kernel for Jupyter notebooks
============================================

Robot Framework language support for Jupyter notebooks.

Requires Python 3.6 or later.


Try Robot Framework kernel at Binder
------------------------------------

Jupyter Notebook: https://mybinder.org/v2/gh/datakurre/robotkernel/master?urlpath=tree/example.ipynb

Jupyter Lab: https://mybinder.org/v2/gh/datakurre/robotkernel/master?urlpath=lab/tree/example.ipynb


Install Robot Framework kernel
------------------------------

.. code:: bash

   $ pip install robotkernel
   $ python -m robotkernel.install


Install Robot Framework kernel from Python 3 notebook
-----------------------------------------------------

.. code:: bash

   !pip install robotkernel
   !python -m robotkernel.install

After refreshing the notebook, it is possible change the kernel to Robot
Framework kernel or create a new notebook with Robot Framework kernel.


Nix-shell (https://nixos.org/nix/)
----------------------------------

.. code:: bash

   $ nix-shell -E 'import (fetchTarball https://github.com/datakurre/robotkernel/archive/master.tar.gz + "/shell.nix")' --run "jupyter notebook"


Local installation and development
----------------------------------

See also: http://jupyter.readthedocs.io/en/latest/install.html

Create and activate clean Python virtual environment::

    $ venv myenv
    $ source myenv/bin/activate

Install Jupyter::

    $ pip install --upgrade pip setuptools
    $ pip install jupyter

Clone this kernel::

    $ git clone https://github.com/datakurre/robotkernel.git
    $ cd robotkernel

Install the kernel into virtualenv in develop mode::

    $ python setup.py develop

Install the kernel into jupyter::

    $ python -m robotkernel.install

Launch the jupyter::

    $ jupyter notebook

Reloading the kernel reloads the code.

Changelog
=========

0.3.2 (2018-09-25)
------------------

- Change to always send display data updates in text/html to workaround a bug
  that caused 'undefined' to be rendered in JupyterLab
  [datakurre]

0.3.1 (2018-09-24)
------------------

- Update README
  [datakurre]

0.3.0 (2018-09-23)
------------------

- First release.
  [datakurre]


