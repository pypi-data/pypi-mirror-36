# jupyter-button_execute

Jupyter notebook button to execute subsequent cells

## Installation

To install use pip:

    $ pip install button_execute
    $ jupyter nbextension enable --py --sys-prefix button_execute


For a development installation (requires npm),

    $ git clone https://github.com/ProtProtocols/jupyter-button_execute.git
    $ cd jupyter-button_execute
    $ pip install -e .
    $ jupyter nbextension install --py --symlink --sys-prefix button_execute
    $ jupyter nbextension enable --py --sys-prefix button_execute

## Usage

To use the button in a notebook, simply execute the following lines in a Jupyter python cell:

``` python
    def my_function(arg):
       print("Hello")
       
       # simply disable the button by setting the 'disabled' variable
       my_btn.disabled = True

   from button_execute import ExecuteButton
   # when clicking the button, the next 3 Jupyter notebook cells will be executed
   my_btn = ExecuteButton(button_text="Run analysis", n_next_cells=3)
   
   # if you register a callback function, this function will be executed
   # before the subsequent cells are being executed
   my_btn.on_click(my_function)
```
   
## Changelog

### Version 0.3

  * Introduced a more reliable method to detect the widget's own cell index

### Version 0.2

  * Added "disabled" property
  * Added callback "on_click" which is triggered before the subsequent
    cells are executed.

### Version 0.1

  * First release
