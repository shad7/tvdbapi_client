"""Provide API client for TVDB API v2.0 services."""
import json
import logging

import cachecontrol
from cachecontrol import caches
from oslo_config import cfg
import requests
import six

from tvdbapi_client import exceptions
from tvdbapi_client import timeutil

LOG = logging.getLogger(__name__)

cfg.CONF.import_group('tvdb', 'tvdbapi_client.options')

DEFAULT_HEADERS = {
    'Accept-Language': 'en',
    'Content-Type': 'application/json',
}

SERIES_BY = [
    'name',
    'imdbId',
    'zap2itId',
]

EPISODES_BY = [
    'airedSeason',
    'airedEpisode',
    'imdbId',
    'dvdSeason',
    'dvdEpisode',
    'absoluteNumber',
    'page',
]


def requires_auth(func):
    """Handle authentication checks.

    .. py:decorator:: requires_auth

        Checks if the token has expired and performs authentication if needed.
    """
    @six.wraps(func)
    def wrapper(self, *args, **kwargs):
        if self.token_expired:
            self.authenticate()
        return func(self, *args, **kwargs)
    return wrapper


class TVDBClient(object):

    """TVDB Api client."""

    def __init__(self, apikey=None, username=None, userpass=None):
        """Create new instance of API client.

        :param str apikey: apikey from thetvdb
        :param str username: username used on thetvdb
        :param str userpass: password used on thetvdb
        """
        self.__apikey = apikey or cfg.CONF.tvdb.apikey
        self.__username = username or cfg.CONF.tvdb.username
        self.__userpass = userpass or cfg.CONF.tvdb.userpass
        self.__token = None

        self._token_timer = None
        self._session = None
        self._headers = DEFAULT_HEADERS
        self._language = 'en'

    @property
    def headers(self):
        """Provide access to updated headers."""
        self._headers.update(**{'Accept-Language': self.language})
        if self.__token:
            self._headers.update(
                **{'Authorization': 'Bearer %s' % self.__token})
        return self._headers

    @property
    def language(self):
        """Provide access to current language."""
        return self._language

    @language.setter
    def language(self, abbr):
        """Provide access to update language."""
        self._language = abbr

    @property
    def token_expired(self):
        """Provide access to flag indicating if token has expired."""
        if self._token_timer is None:
            return True
        return timeutil.is_newer_than(self._token_timer, timeutil.ONE_HOUR)

    @property
    def session(self):
        """Provide access to request session with local cache enabled."""
        if self._session is None:
            self._session = cachecontrol.CacheControl(
                requests.Session(),
                cache=caches.FileCache('.tvdb_cache'))
        return self._session

    @exceptions.error_map
    def _exec_request(self, service, method=None, path_args=None, data=None,
                      params=None):
        """Execute request."""
        if path_args is None:
            path_args = []

        req = {
            'method': method or 'get',
            'url': '/'.join(str(a).strip('/') for a in [
                cfg.CONF.tvdb.service_url, service] + path_args),
            'data': json.dumps(data) if data else None,
            'headers': self.headers,
            'params': params,
            'verify': cfg.CONF.tvdb.verify_ssl_certs,
        }

        LOG.debug('executing request (%s %s)', req['method'], req['url'])
        resp = self.session.request(**req)

        resp.raise_for_status()
        return resp.json() if resp.text else resp.text

    def _login(self):
        data = {'apikey': self.__apikey,
                'username': self.__username,
                'userkey': self.__userpass,
                }
        return self._exec_request('login', method='post', data=data)

    def _refresh_token(self):
        return self._exec_request('refresh_token')

    def authenticate(self):
        """Aquire authorization token for using thetvdb apis."""
        if self.__token:
            try:
                resp = self._refresh_token()
            except exceptions.TVDBRequestException as err:
                # if a 401 is the cause try to login
                if getattr(err.response, 'status_code', 0) == 401:
                    resp = self._login()
                else:
                    raise
        else:
            resp = self._login()

        self.__token = resp.get('token')
        self._token_timer = timeutil.utcnow()

    @requires_auth
    def search_series(self, **kwargs):
        """Provide the ability to search for a series.

        .. warning::

            authorization token required

        The following search arguments currently supported:

            * name
            * imdbId
            * zap2itId

        :param kwargs: keyword arguments to search for series
        :returns: series record or series records
        :rtype: dict
        """
        params = {}
        for arg, val in six.iteritems(kwargs):
            if arg in SERIES_BY:
                params[arg] = val
        resp = self._exec_request(
            'search', path_args=['series'], params=params)
        if cfg.CONF.tvdb.select_first:
            return resp['data'][0]
        return resp['data']

    @requires_auth
    def get_series(self, series_id):
        """Retrieve series record.

        .. warning::

            authorization token required

        :param str series_id: id of series as found on thetvdb
        :returns: series record
        :rtype: dict
        """
        return self._exec_request('series', path_args=[series_id])['data']

    @requires_auth
    def get_episodes(self, series_id, **kwargs):
        """All episodes for a given series.

        Paginated with 100 results per page.

        .. warning::

            authorization token required

        The following search arguments currently supported:

            * airedSeason
            * airedEpisode
            * imdbId
            * dvdSeason
            * dvdEpisode
            * absoluteNumber
            * page

        :param str series_id: id of series as found on thetvdb
        :parm kwargs: keyword args to search/filter episodes by (optional)
        :returns: series episode records
        :rtype: list
        """
        params = {'page': 1}
        for arg, val in six.iteritems(kwargs):
            if arg in EPISODES_BY:
                params[arg] = val
        return self._exec_request(
            'series',
            path_args=[series_id, 'episodes', 'query'], params=params)['data']

    @requires_auth
    def get_episodes_summary(self, series_id):
        """Return a summary of the episodes and seasons for the series.

        .. warning::

            authorization token required

        .. note::

            Season "0" is for all episodes that are considered to be specials.

        :param str series_id: id of series as found on thetvdb
        :returns: summary of the episodes and seasons for the series
        :rtype: dict
        """
        return self._exec_request(
            'series', path_args=[series_id, 'episodes', 'summary'])['data']

    @requires_auth
    def get_series_image_info(self, series_id):
        """Return a summary of the images for a particular series.

        .. warning::

            authorization token required

        :param str series_id: id of series as found on thetvdb
        :returns: summary of the images for the series
        :rtype: dict
        """
        return self._exec_request(
            'series', path_args=[series_id, 'images'])['data']

    @requires_auth
    def get_episode(self, episode_id):
        """Return the full information for a given episode id.

        .. warning::

            authorization token required

        :param str episode_id: id of episode as found on thetvdb
        :returns: episode record
        :rtype: dict
        """
        return self._exec_request('episodes', path_args=[episode_id])['data']
