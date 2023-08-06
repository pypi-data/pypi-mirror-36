|Show Logo|

============
text-summary
============

|build| |coverage| |docs| |release|

Summarize blocks of text using NLTK tools

Getting Started
---------------

.. code-block:: bash

    pip install .
    summarize --dump_config > app_local.cfg  # for writing secrets
    summarize --config=app_local.cfg 

Meant to be installed directly or into a thin client for easy cronjobs/CLI.  

Powered by `plumbum`_

Features
========

TODO

.. _plumbum: http://plumbum.readthedocs.io/en/latest/cli.html

.. |Show Logo| image:: http://dl.eveprosper.com/podcast/logo-colour-17_sm2.png
    :target: http://eveprosper.com
.. |build| image:: https://travis-ci.org/lockefox/text-summary.svg?branch=master
    :target: https://travis-ci.org/lockefox/text-summary
.. |coverage| image:: https://coveralls.io/repos/github/lockefox/text-summary/badge.svg?branch=master
    :target: https://coveralls.io/github/lockefox/text-summary?branch=master
.. |docs| image:: https://readthedocs.org/projects/text-summary/badge/?version=latest
    :target: https://text-summary.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status