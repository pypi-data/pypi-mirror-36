
**reelog python log best practices**

.. code-block:: python

    >>> import reelog
    >>> # root logger
    >>> logger = reelog.get_logger()
    >>> logger.info("hello world!")
    >>> # reelog name logger
    >>> logger = reelog.get_logger("reelog")
    >>> logger.error("hello world!")
    >>> # output to stdout and file
    >>> logger = reelog.get_logger("reelog", stdout=Ture, file=Ture)
    >>> logger.warning("hello world!")
    >>> # output to stdout and rotate file
    >>> logger = reelog.get_logger("reelog", stdout=Ture, rotate_file=Ture)
    >>> logger.warning("hello world!")
