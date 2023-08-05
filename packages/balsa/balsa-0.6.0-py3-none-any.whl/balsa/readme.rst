.. this file is kept in the docs\source directory and COPIED to the project directories (root and/or package).
.. DO NOT edit the copy in the project root directory or the package directory..

balsa (logging utility)
=======================

Simple to use package that sets up Python logging.  With just a few lines of code get well formatted file and
console or GUI logging.


Simple Example
==============

.. code:: python

    from balsa import get_logger, Balsa

    application_name = 'example'

    log = get_logger(application_name)


    def main():
        balsa = Balsa(application_name, 'james abel')
        balsa.init_logger()
        log.error('my error example')


This will yield output of this form:

.. code-block:: console

    2018-04-15 11:25:58,507 - example - balsa_simple_example.py - 12 - main - ERROR - my error example


Where did the name come from?
=============================
Balsa lumber is very soft and light, with a coarse, open grain.
The Balsa package is light weight, malleable, and open source.
