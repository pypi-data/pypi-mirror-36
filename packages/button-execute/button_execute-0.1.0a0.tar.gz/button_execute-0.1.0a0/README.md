jupyter-button_execute
===============================

Jupyter notebook button to execute subsequent cells

Installation
------------

To install use pip:

    $ pip install button_execute
    $ jupyter nbextension enable --py --sys-prefix button_execute


For a development installation (requires npm),

    $ git clone https://github.com/ProtProtocols/jupyter-button_execute.git
    $ cd jupyter-button_execute
    $ pip install -e .
    $ jupyter nbextension install --py --symlink --sys-prefix button_execute
    $ jupyter nbextension enable --py --sys-prefix button_execute
