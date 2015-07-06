TVDB Api Client
===============

.. image:: https://travis-ci.org/shad7/tvdbapi_client.svg?branch=develop
    :target: https://travis-ci.org/shad7/tvdbapi_client

.. image:: https://coveralls.io/repos/shad7/tvdbapi_client/badge.svg?branch=develop
  :target: https://coveralls.io/r/shad7/tvdbapi_client?branch=develop


Python client for theTVDB API (v1.2+) REST endpoints in json format.


Features
--------

* provide client for interacting with thetvdb api


Usage
-----

        >>> import tvdbapi_client
        >>> client = tvdbapi_client.get_client(apikey='abc123', username='johndoe', userpass='mypass')
        >>> client.search_series('the big bang theory')
        [{'status': 'Continuing', 'network': 'CBS', 'overview': "What happens when hyperintelligent roommates Sheldon and Leonard meet Penny, a free-spirited beauty moving in next door, and realize they know next to nothing about life outside of the lab. Rounding out the crew are the smarmy Wolowitz, who thinks he's as sexy as he is brainy, and Koothrappali, who suffers from an inability to speak in the presence of a woman.", 'seriesName': 'The Big Bang Theory', 'firstAired': '2007-09-24', 'poster': 'graphical/80379-g23.jpg', 'id': 80379, 'aliases': ['Big Bang']}]

        >>> from tvdbapi_client import api
        >>> client = api.TVDBClient(apikey='abc123', username='johndoe', userpass='mypass')
        >>> client.search_series('the big bang theory')
        [{'status': 'Continuing', 'network': 'CBS', 'overview': "What happens when hyperintelligent roommates Sheldon and Leonard meet Penny, a free-spirited beauty moving in next door, and realize they know next to nothing about life outside of the lab. Rounding out the crew are the smarmy Wolowitz, who thinks he's as sexy as he is brainy, and Koothrappali, who suffers from an inability to speak in the presence of a woman.", 'seriesName': 'The Big Bang Theory', 'firstAired': '2007-09-24', 'poster': 'graphical/80379-g23.jpg', 'id': 80379, 'aliases': ['Big Bang']}]


Available Configuration Options
-------------------------------

- **apikey**::

        API key from your TVDB account.

        Default: ENV['TVDB_API_KEY']

- **username**::

        Username from your TVDB account.

        Default: ENV['TVDB_USERNAME']

- **userpass**::

        Password from your TVDB account.

        Default: ENV['TVDB_PASSWORD']

- **service_url**::

        Base URL for TVDB API service.

        Default: https://api-dev.thetvdb.com

- **verify_ssl_certs**::

        Flag for validating ssl certs for service url (https).

        Default: True

- **select_first**::

        Flag for selecting first series from search results.

        Default: False


Configuring service can be done by either of the following:

* passing individual inputs directly to `tvdbapi_client.get_client`
* passing path to configuration file to `tvdbapi_client.get_client`
* setting environment variables as noted above


Documentation
-------------

Documentation is available at http://tvdbapi-client.readthedocs.org/.

