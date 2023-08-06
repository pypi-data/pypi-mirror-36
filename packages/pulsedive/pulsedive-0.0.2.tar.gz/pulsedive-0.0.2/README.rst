Python Pulsedive Client
===========================

A low-level Python client for Pulsedive that aims provide an easy and idiomatic way to interact with the Pulsedive API.


Installation
------------

Install the ``pulsedive`` package with `pip
<https://pypi.org/project/pulsedive/>`_::

    pip install pulsedive


Example use
-----------

Simple use-case::

    import pulasedive
    pud = pulsedive.Pulsedive()

    # Getting a specific indicator
    ind = pud.indicator(name='pulsedive.com')
    pud.indicator.links(ind['iid'])

    # Searching for indicators
    pud.search('pulsedive', risks=['high', 'critical'], indicator_type=['ip'])


    # Pulling from feeds or threats
    pud.feed.links(1)
    pud.threat.links(1)

    # Searching for threats and feeds
    pud.search.threat('Zeus')
    pud.search.feed('Zeus')



`Full documentation`_.

.. _Full documentation: https://pulsedive-py.readthedocs.io