TVDB Api Client
===============

.. image:: https://readthedocs.org/projects/tvdbapi-client/badge/?version=latest
    :target: https://readthedocs.org/projects/tvdbapi-client/?badge=latest

.. image:: https://travis-ci.org/shad7/tvdbapi_client.svg?branch=develop
    :target: https://travis-ci.org/shad7/tvdbapi_client

.. image:: https://coveralls.io/repos/shad7/tvdbapi_client/badge.svg?branch=develop
    :target: https://coveralls.io/r/shad7/tvdbapi_client?branch=develop

.. image:: https://requires.io/github/shad7/tvdbapi_client/requirements.svg?branch=develop
    :target: https://requires.io/github/shad7/tvdbapi_client/requirements/?branch=develop


Python client for theTVDB API (v1.2+) REST endpoints in json format.

`TVDB Api Client Documentation <http://tvdbapi-client.readthedocs.org/>`_


Features
^^^^^^^^

* provide client for interacting with thetvdb api


Usage
^^^^^

        >>> import tvdbapi_client
        >>> client = tvdbapi_client.get_client(apikey='abc123', username='johndoe', userpass='mypass')
        >>> client.search_series(name='the big bang theory')
        [{'status': 'Continuing', 'network': 'CBS', 'overview': "What happens when hyperintelligent roommates Sheldon and Leonard meet Penny, a free-spirited beauty moving in next door, and realize they know next to nothing about life outside of the lab. Rounding out the crew are the smarmy Wolowitz, who thinks he's as sexy as he is brainy, and Koothrappali, who suffers from an inability to speak in the presence of a woman.", 'seriesName': 'The Big Bang Theory', 'firstAired': '2007-09-24', 'poster': 'graphical/80379-g23.jpg', 'id': 80379, 'aliases': ['Big Bang']}]

        >>> from tvdbapi_client import api
        >>> client = api.TVDBClient(apikey='abc123', username='johndoe', userpass='mypass')
        >>> client.search_series(name='the big bang theory')
        [{'status': 'Continuing', 'network': 'CBS', 'overview': "What happens when hyperintelligent roommates Sheldon and Leonard meet Penny, a free-spirited beauty moving in next door, and realize they know next to nothing about life outside of the lab. Rounding out the crew are the smarmy Wolowitz, who thinks he's as sexy as he is brainy, and Koothrappali, who suffers from an inability to speak in the presence of a woman.", 'seriesName': 'The Big Bang Theory', 'firstAired': '2007-09-24', 'poster': 'graphical/80379-g23.jpg', 'id': 80379, 'aliases': ['Big Bang']}]

