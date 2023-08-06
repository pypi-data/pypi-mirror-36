# logging-bootstrap

Library to provide simple methods to bootstrap logger with default settings.

## How to install

In your __main__.py module add:

* import logging

*  import loggingbootstrap

* loggingbootstrap.create_double_logger("toplevelmodule", logging.INFO, "example.log",
                                      logging.DEBUG)

NOTE: This step is only required to do once.

## How to use logger

After the previous configuration just use logger like this:

* logger = logging.getLogger(__name__) # this will associate with the top level module

* logger.debug("hello world")

Result (example):

* 05/08/2016 04:38:55 | DEBUG | pycontrolgui.windows.detail.entities.setup_window | _combo_board_item_changed | _combo_board_item_changed