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

Usage
-----

To use the button in a notebook, simply execute the following lines in a Jupyter python cell:

``` python
   from button_execute import ExecuteButton
   # when clicking the button, the next 3 Jupyter notebook cells will be executed
   ExecuteButton(button_text="Run analysis", n_next_cells=3)
```
   
