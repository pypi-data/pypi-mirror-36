===================
python-ripple-lib
===================
Description
------------

python-ripple-rpc is a small client library to access Ripple `rippled API <https://developers.ripple.com/rippled-api.html>`_.
Currently it supports public and admin methods (some of them still are work in progress though). List of implemented methods will be displayed below.
Basically, it's just a wrapper on top of http requests made to API.

Installation
-------------

To install the package from PyPi run the following command

::

    pip install python-ripple-lib

If you want to install package from this repo, use ``setup.py``

::

    python setup.py install

If you want to install package just for development purposes, use another command

::

    python setup.py develop

This command creates symlinks to package files instead of copying it to package directory

JSON-RPC Methods
----------------

| Most of JSON-RPC methods are implemented inside, for the full list of methods please refer to list of `Public <https://developers.ripple.com/public-rippled-methods.html>`_ and `Admin <https://developers.ripple.com/admin-rippled-methods.html>`_ methods from ripple documentation
| How to use:

.. code-block:: python3

    from ripple_api import RippleRPCClient

    rpc = RippleRPCClient('http://s1.ripple.com:51234/')
    account_info = rpc.account_info('r9cZA1mLK5R5Am25ArfXFmqgNwjZgnfk59')


Data API Methods
----------------

| Most of Data API requests are implemented here as well, fll list located in `here <https://developers.ripple.com/data-api.html>`_
| How to use:

.. code-block:: python

    from ripple_api import RippleDataAPIClient

    api = RippleDataAPIClient('https://data.ripple.com')
    identifier = '3170DA37CE2B7F045F889594CBC323D88686D2E90E8FFD2BBCD9BAD12E416DB5'
    query_params = dict(transactions='true')
    ledger_info = api.get_ledger(ledger_identifier=identifier, **query_params)


