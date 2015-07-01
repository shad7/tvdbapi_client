TVDB Api Client
===============

Python client for thetvdb api (v1.2+)


Features
--------

* provide client for interacting with thetvdb api


Usage
-----

        >>> import tvdbapi_client
        >>> client = tvdbapi_client.get_client(apikey='abc123', username='johndoe', userpass='mypass')
        >>> client.search_series('the big bang theory')
        [{'status': 'Continuing', 'network': 'CBS', 'overview': "What happens when hyperintelligent roommates Sheldon and Leonard meet Penny, a free-spirited beauty moving in next door, and realize they know next to nothing about life outside of the lab. Rounding out the crew are the smarmy Wolowitz, who thinks he's as sexy as he is brainy, and Koothrappali, who suffers from an inability to speak in the presence of a woman.", 'seriesName': 'The Big Bang Theory', 'firstAired': '2007-09-24', 'poster': 'graphical/80379-g23.jpg', 'id': 80379, 'aliases': ['Big Bang']}]


Contents:

.. toctree::
    :maxdepth: 1

    ChangeLog
    source


Indices and tables
==================

* :ref:`genindex`
* :ref:`search`

