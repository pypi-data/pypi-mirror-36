================
CacheLite
================

Documentation
-------------

The full documentation is at https://cachelite.readthedocs.org/

Quickstart
----------

Install cachelite::

    pip install cachelite

Then you can use it.

.. code-block:: python

    import cachelite from CacheLite

    cache = CacheLite("/tmp/YOUR_TO_CACHE_DIR")

    #put a key-value
    cache["YOUR_KEY"] = "YOUR_VALUE"

    #get a value
    value = cache["YOUR_KEY"]

    #delete a value
    del cache["YOUR_KEY"]

    #get size of data entries
    len(cache)

    #iteration
    for a in cache:
        print(a)

